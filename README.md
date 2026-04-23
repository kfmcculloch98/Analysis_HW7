# HOW TO CREATE A CLONE OF THIS REPOSITORY

1. Create a new GitHub repository (repo).
2. Copy **this** repo https url to clipboard.
3. Clone this repo by running this line in your terminal after navigating to the desired working directory:
```git clone <https url>```

# HOW TO SET UP A VIRTUAL ENVIRONMENT (LOCAL)

1. Create a virtual environment named 'hw7_forecast' by running this line in your terminal:
```python -m venv hw7_forecast```
2. Activate the environment by running these two lines:
```Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser```
```.\hw7_forecast\Scripts\activate```
3. Copy over requirements.txt then run:
```pip install -r requirements.txt```
4. Run this if you install additional libraries:
```pip freeze > requirements.txt```

# HOW TO SET UP A VIRTUAL ENVIRONMENT (CODESPACE)

1. Create a virtual environment by running this line in the bash terminal:
```python -m venv .venv```
2. Activate the environment by running this line:
```source .venv/bin/activate```
3. Copy over requirements.txt then run:
```pip install -r requirements.txt```
4. Run this if you install additional libraries:
```pip freeze > requirements.txt```
