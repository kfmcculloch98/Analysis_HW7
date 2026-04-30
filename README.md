# How to Create a Clone of This GitHub Repoistory

1. Create a new GitHub repository (repo).
2. Copy **this** repo https url to clipboard.
3. Clone this repo by running this line in your terminal after navigating to the desired working directory:
```git clone <https url>```

# How to Set Up a Virtual Environment on a Local PC

1. Create a virtual environment named 'hw7_forecast' by running this line in your terminal:
```python -m venv hw7_forecast```
2. Activate the environment by running these two lines:
```Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser```
```.\hw7_forecast\Scripts\activate```
3. Ensure requirements.txt exists (it should copy over when you clone) then run:
```pip install -r requirements.txt```
4. Run this if you install additional libraries:
```pip freeze > requirements.txt```

# How to Set Up a Virtual Environment on a Codespace

1. Create a virtual environment by running this line in the bash terminal:
```python -m venv .venv```
2. Activate the environment by running this line:
```source .venv/bin/activate```
3. Ensure requirements.txt exists (it should copy over when you clone) then run:
```pip install -r requirements.txt```
4. Run this if you install additional libraries:
```pip freeze > requirements.txt```

# How to Run a Shell Script on a Local PC

1. Run the script by running this line:
```bash run_workflow.sh``` or
```wsl ./run_workflow.sh```

3. Follow the prompts for user input.

# How to Run a Shell Script on a Codespace

1. Make the script executable by running line in the bash terminal:
```chmod +x run_workflow.sh```
2. Run the script by running this line:
```./run_workflow.sh```
3. Follow the prompts for user input.


