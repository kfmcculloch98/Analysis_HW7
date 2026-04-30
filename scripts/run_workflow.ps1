# =============================================================================
# BACK END OPTIONS
# =============================================================================

$env:MPLBACKEND = "Agg" # Write plots to disk but do not display them as the script runs

# =============================================================================
# USER OPTIONS
# =============================================================================

Write-Host "--- Streamflow Forecast Configuration ---" -ForegroundColor Cyan

$Email      = Read-Host -Prompt "Enter your HydroFrame login email"
$Pin        = Read-Host -Prompt "Enter your HydroFrame PIN"
$GaugeId    = Read-Host -Prompt "Enter Gauge ID [e.g.: 09506000 (Verde River)]"
if ([string]::IsNullOrWhiteSpace($GaugeId)) { $GaugeId = "09506000" }

$ArOrder    = Read-Host -Prompt "Enter AR Order (Lag days) [Default: 7]"
if ([string]::IsNullOrWhiteSpace($ArOrder)) { $ArOrder = "7" }

$TrainStart = Read-Host -Prompt "Enter Training Start Date (YYYY-MM-DD) [Default: 1990-01-01]"
if ([string]::IsNullOrWhiteSpace($TrainStart)) { $TrainStart = "1990-01-01" }

$TrainEnd   = Read-Host -Prompt "Enter Training End Date (YYYY-MM-DD) [Default: 2022-12-31]"
if ([string]::IsNullOrWhiteSpace($TrainEnd)) { $TrainEnd = "2022-12-31" }

$TestStart  = Read-Host -Prompt "Enter Test Start Date (YYYY-MM-DD) [Default: 2023-01-01]"
if ([string]::IsNullOrWhiteSpace($TestStart)) { $TestStart = "2023-01-01" }

$TestEnd    = Read-Host -Prompt "Enter Test End Date (YYYY-MM-DD) [Default: 2024-12-31]"
if ([string]::IsNullOrWhiteSpace($TestEnd)) { $TestEnd = "2024-12-31" }

$ForecastDate = Read-Host -Prompt "Enter Forecast Date (YYYY-MM-DD) [Default: 2024-04-30]"
if ([string]::IsNullOrWhiteSpace($ForecastDate)) { $ForecastDate = "2024-04-30" }

$Refit      = Read-Host -Prompt "Refit Model? (True/False) [Default: True]"
if ([string]::IsNullOrWhiteSpace($Refit)) { $Refit = "True" }

$Validate   = Read-Host -Prompt "Run Validation? (True/False) [Default: True]"
if ([string]::IsNullOrWhiteSpace($Validate)) { $Validate = "True" }

$Model      = Read-Host -Prompt "Enter Model (markov, monthly_avg, longterm_avg) [Default: markov]"
if ([string]::IsNullOrWhiteSpace($Model)) { $Model = "markov" }

$NStates    = Read-Host -Prompt "Enter number of Markov states [Default: 5]"
if ([string]::IsNullOrWhiteSpace($NStates)) { $NStates = "5" }

# --- Execution Section ---

Write-Host "`n--- Running Train Model ---" -ForegroundColor Yellow
python train_model.py `
    --email $Email `
    --pin $Pin `
    --gauge-id $GaugeId `
    --n-states $NStates `
    --ar-order $ArOrder `
    --train-start $TrainStart `
    --train-end $TrainEnd `
    --test-start $TestStart `
    --test-end $TestEnd `
    --model $Model `
    --refit $Refit `
    --validate $Validate

if ($LASTEXITCODE -ne 0) { 
    Write-Host "`nTraining failed. Script stopped." -ForegroundColor Red
    exit 
}

Write-Host "`n--- Running Generate Forecast ---" -ForegroundColor Yellow
python generate_forecast.py `
    --email $Email `
    --pin $Pin `
    --gauge-id $GaugeId `
    --ar-order $ArOrder `
    --forecast-date $ForecastDate `
    --model $Model

Write-Host "`nWorkflow Complete!" -ForegroundColor Green
