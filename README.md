# SETTING UP A CLONE OF THIS REPOSITORY AND YOUR VIRTUAL ENVIRONMENT

1. Create a new GitHub repository (repo).
2. Copy **this** repo https url to clipboard.
3. Clone this repo by running this line in your terminal after navigating to the desired working directory:
```git clone <https url>```
4. Create a virtual environment named 'hw7_forecast' by running this line in your terminal:
```python -m venv hw7_forecast```
5. Activate the environment by running these two lines:
```Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser```
```.\hw7_forecast\Scripts\activate```
7. Copy over requirements.txt then run:
```pip install -r requirements.txt```
8. Run this if you install additional libraries:
```pip freeze > requirements.txt```
