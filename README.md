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

## App Installation

Before running any scripts, make sure to check if you have Python installed on your machine. If you aren't sure, 
{download the latest version of Python](https://www.python.org/downloads/) and install it on your system.

If you are running Windows on your machine, it is also necessary to have Git Bash for Windows installed. 
If you don't have it already, please [download the latest version](https://git-scm.com/downloads) and install it on your system.

The easiest way to clone the repository is to use the HTTPS method. When inside of your preferred shell 
(Git Bash, Bash, zsh, ect), use the command ```git clone https://github.com/cmadajski/niner_miner.git``` 
and the files will be downloaded to your local system.

For more advanced users, SSH is an even better way to interact with GitHub repos. For detailed instructions 
on using SSH with GitHub, [check out this webpage.](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

For your convenience, we made a single script that creates a virtual environment, installs dependencies, 
and creates the database automatically. In the niner_miner directory, open the ```install``` directory. 
- if you are using Git Bash for Windows, use the command ```./app_install_windows_gitbash.sh```
- if you are using Mac(zsh) or Linux(bash, dash, etc), use the command ```./app_install_mac_linux.sh```

Once you run the above script you must manually activate the virtual environment by navigating to the ```niner_miner``` directory and using the command ```source env/Scripts/activate``` on Windows machines or ```source env/bin/activate``` on Mac/Linux to start the virtual environment.

## Running the Code
Navigate to the ```src``` directory. Then use the command ```python main.py``` to start
the development server and allow access to the app.

An IP Address should be visible in the console, and you can either ctl+click the address
or copy and paste the address into a web browser to view the app. You can also manually
enter this address into your webbrowser if needed: ```http://127.0.0.1:5000/```

## Resetting the Database
While we are in the process of building and testing the application, it is sometimes necessary to delete and 
rebuild the database to remove existing data and start from scratch. To simplify this process, a script in the
```src/``` directory named reset_db.py automates the process of resetting the database. This should only be necessary if any models change or new models are added.

To reset the command the command ```python reset_db.py```

## Work in Progress
At this time in development, the application still has most of its functions non-operational.
We are hoping to have most functions working as intended by the last week of April.
