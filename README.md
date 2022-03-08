# Niner Miner - E-commerce for UNCC Students

This web application is a project created for ITSC 4155 Software Engineering Capstone.
The goal is to create an e-commerce platform similar to OfferUp and Craigslist that allows for UNCC
students to buy and sell personal goods. The unique feature we seek to offer is using
UNCC email verification to ensure that only legitimate UNCC students are involved in
buying and selling. This helps overcome the issue of anonymity that causes so many
problems on already existing services. Our service will provide an additional layer of
security and trust to students and incentivize them to use our platform instead of the
competitors.

The contributing members for this project are:
- Oviya Manoharan
- Hinal Makadiya
- Dane Medlin
- Drew Moore
- [Christian Madajski](https://www.linkedin.com/in/cmadajsk/) [![wakatime](https://wakatime.com/badge/user/510092ca-a9b8-48f5-bf50-9b05005ef525/project/a5b9008a-d413-431f-92d4-80beef67c7cc.svg)](https://wakatime.com/badge/user/510092ca-a9b8-48f5-bf50-9b05005ef525/project/a5b9008a-d413-431f-92d4-80beef67c7cc)

The technologies being used are:
- Python/Flask (Backend + Logic)
- SQLAlchemy (Database)
- HTML/CSS/JS (Frontend)
- Google Maps (Mapping)
- PayPal (Purchases)

## Installing Dependencies
In order to get the back end working we need to get a virtual environment running, so we can install the 
necessary dependencies. Assuming you are using Git Bash on Windows, we can use the command 
```python -m venv env``` to create a python 
virtual environment in your current directory.
Additional information on virtual environments can be found 
[here](https://docs.python.org/3/library/venv.html). Then you can activate the venv by typing:
- Git Bash on Windows: ```source env/Scripts/activate```
- Bash on Linux: ```source env/bin/activate```

Once the venv is activated, then we can install the necessary dependencies. This repo includes
a file named "requirements.txt" that can be used to automatically install all necessary libraries.
The easiest way to do this is to first CD into the directory that contains requirements.txt.
Then use the below command to install the requirements:

```pip install -r /path/to/requirements.txt```

For additional troubleshooting, refer to [this page](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/).

## Running the Code
This app uses the Flask framework as a backend, so you must start a local development
server to get the app up and working. The way the app is currently set up, just navigate
to the niner_miner directory and run the command ```python run.py``` to start the server.
An IP Address should be visible in the console, and you can either ctl+click the address
or copy and paste the address into a web browser to view the app. You can also manually
enter this address into your webbrowser if needed: ```http://127.0.0.1:5000/```
