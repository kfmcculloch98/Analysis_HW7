# SETTING UP REPOSITORY AND ENVIRONMENT

# create a new GitHub repository (repo)

# copy repo https url

# clone the epo by running this line in your terminal after navigating to the desired working directory
git clone <https url>

# create a virtual environment named 'hw7_forecast' by running this line in your terminal:
python -m venv hw7_forecast

# activate the environment by running these two lines:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\hw7_forecast\Scripts\activate

# copy over requirements.txt then run:
pip install -r requirements.txt

# run this if you install additional libraries:
pip freeze > requirements.txt