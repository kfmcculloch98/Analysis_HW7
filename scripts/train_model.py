"""
train_model.py
--------------
Fits the chosen model on the training period and optionally validates on the
test period. Run via run_workflow.sh, or directly:

    python train_model.py --email YOU@EMAIL.COM --pin 1234 [--other-options]
"""

import os
import argparse
import pandas as pd
import hf_hydrodata
import numpy as np
from forecast_functions import (
    get_training_test_data,
    fit_longterm_avg_model,
    fit_monthly_avg_model,
    fit_markov_model,
    compute_metrics,
    plot_validation,
    save_model,
    load_model,
)

parser = argparse.ArgumentParser()
parser.add_argument('--email',       required=True)
parser.add_argument('--pin',         required=True)
parser.add_argument('--gauge-id',    default='09506000')
parser.add_argument('--ar-order',    type=int, default=7)
parser.add_argument('--train-start', default='1990-01-01')
parser.add_argument('--train-end',   default='2022-12-31')
parser.add_argument('--test-start',  default='2023-01-01')
parser.add_argument('--test-end',    default='2024-12-31')
parser.add_argument('--model',       default='longterm_avg', choices=['longterm_avg', 'monthly_avg', 'markov'])
parser.add_argument('--refit',       default='True')
parser.add_argument('--validate',    default='True')
parser.add_argument('--n-states', type=int, default=5, help='Number of states for Markov Chain')
args = parser.parse_args()
args = parser.parse_args()

REFIT_MODEL    = args.refit.lower()    == 'true'
RUN_VALIDATION = args.validate.lower() == 'true'

hf_hydrodata.register_api_pin(email=args.email, pin=args.pin)

print("\n--- Step 1: Download streamflow data ---")
train, test = get_training_test_data(
    args.gauge_id, args.train_start, args.train_end,
    args.test_start, args.test_end
)

# ── Fitting model ───────────────────────────────────────────────────
if args.model == 'longterm_avg':
    print("\n--- Step 2: Fit long-term average model ---")
    if REFIT_MODEL or not os.path.exists('saved_model.pkl'):
        mean_flow = fit_longterm_avg_model(train)
        print(mean_flow)
        print(f"  Long-term mean: {mean_flow:.2f} cfs")
        save_model(mean_flow)
    else:
        mean_flow = load_model()
        if not isinstance(mean_flow, float):
            raise TypeError(
                "saved_model.pkl does not contain a longterm_avg model. "
                "Re-run with --refit True --model longterm_avg to train one."
            )

    if RUN_VALIDATION:
        print("\n--- Step 3: Validate on test period ---")
        train_fitted    = pd.Series(mean_flow, index=train.index)
        forecast_series = pd.Series(mean_flow, index=test.index)

        metrics = compute_metrics(test['streamflow_cfs'].values, forecast_series.values)
        print("\n  Validation metrics:")
        for name, val in metrics.items():
            print(f"    {name:<12}: {val:.4f}")
        print("\n  NSE guide: >0.75 very good | 0.65–0.75 good | "
              "0.50–0.65 satisfactory | <0.50 poor")

        print("\n  Generating validation plot ...")
        plot_validation(
            train['streamflow_cfs'], test['streamflow_cfs'],
            forecast_series, metrics, 'Long-term Average',
            train_forecast_cfs=train_fitted
        )

elif args.model == 'monthly_avg':
    print("\n--- Step 2: Fit monthly average model ---")
    if REFIT_MODEL or not os.path.exists('saved_model.pkl'):
        mean_flow = fit_monthly_avg_model(train)
        print(mean_flow) # to print dictionary
        save_model(mean_flow)
    else:
        mean_flow = load_model()
        if not isinstance(mean_flow, dict):
            raise TypeError(
                "saved_model.pkl does not contain a monthly_avg model. "
                    "Re-run with --refit True --model monthly_avg to train one."
                )

    if RUN_VALIDATION:
        print("\n--- Step 3: Validate on test period ---")
        train.index = pd.to_datetime(train.index)
        test.index = pd.to_datetime(test.index)
        train_fitted = pd.Series([mean_flow[d.month] for d in train.index], index=train.index)
        forecast_series = pd.Series([mean_flow[d.month] for d in test.index], index=test.index)
        metrics = compute_metrics(test['streamflow_cfs'].values, forecast_series.values)
        print("\n  Validation metrics:")
        for name, val in metrics.items():
            print(f"    {name:<12}: {val:.4f}")
        print("\n  NSE guide: >0.75 very good | 0.65–0.75 good | "
              "0.50–0.65 satisfactory | <0.50 poor")

        print("\n  Generating validation plot ...")
        plot_validation(
            train['streamflow_cfs'], test['streamflow_cfs'],
            forecast_series, metrics, 'Monthly Average',
            train_forecast_cfs=train_fitted
        )

elif args.model == 'markov':
    print(f"\n--- Step 2: Fit Markov Chain model with {args.n_states} states ---")
    if REFIT_MODEL or not os.path.exists('saved_model.pkl'):
        # Passing new moddel_dict (containing probability matrix, bins, and medians) instead of mean_flow 
        model_dict = fit_markov_model(train, n_states=args.n_states)
        save_model(model_dict)
    else:
        model_dict = load_model()
        if not isinstance(model_dict, dict) or 'matrix' not in model_dict:
            raise TypeError(
                "saved_model.pkl is not a Markov model.")

    if RUN_VALIDATION:
        print("\n--- Step 3: Validate on test period ---")
        # Simulate a 1-day ahead forecast for every day in the test set
        # See how the transitions perform generally
        bins = model_dict['bins']
        matrix = model_dict['matrix']
        medians = model_dict['medians']

        def predict_next(val):
            state = np.clip(np.digitize(val, bins) - 1, 0, len(matrix)-1)
            next_state = matrix.loc[state].idxmax()
            return np.exp(medians[next_state]) - 1

        forecast_series = test['log_flow'].shift(1).fillna(train['log_flow'].iloc[-1]).apply(predict_next)
        forecast_series.index = test.index

        metrics = compute_metrics(test['streamflow_cfs'].values, forecast_series.values)
        print("\n  Validation metrics (1-day ahead):")
        for name, val in metrics.items():
            print(f"    {name:<12}: {val:.4f}")

        print("\n  Generating validation plot ...")
        plot_validation(
            train['streamflow_cfs'], test['streamflow_cfs'],
            forecast_series, metrics, 'Markov Chain'
        )

print("\nTraining complete.")
