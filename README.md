# Niner Miner - E-commerce for UNCC Students

## Accessing the App

The app is now up and running on a Linode server. Use [this link](http://194.195.214.161/) to access the live demo. To log in, use the following credentials:

email: demo@uncc.edu

password: demo1234

## Summary

This web application is a project created for ITSC 4155 Software Engineering Capstone (Spring 2022).
The goal was to create an e-commerce platform similar to OfferUp and Craigslist that allows for UNCC
students to buy and sell personal goods. The unique feature we seek to offer is using
UNCC email verification to ensure that only legitimate UNCC students are involved in
buying and selling. This helps overcome the pervasive issue of anonymity that is both a boon
and a sourge to Internet users worldwide. Validating users up front adds an additional layer
of trust and security to our platform which will lead to greater community engagement and less
stress for users in the ecosystem.

The contributing members for this project are:
- [Oviya Manoharan](https://github.com/oviya23)
- [Hinal Makadiya](https://www.linkedin.com/in/hinal-makadiya-60838b207/)
- Dane Medlin
- [Drew Moore](https://github.com/drew18moore)
- [Christian Madajski](https://www.linkedin.com/in/cmadajsk/) [![wakatime](https://wakatime.com/badge/user/510092ca-a9b8-48f5-bf50-9b05005ef525/project/a5b9008a-d413-431f-92d4-80beef67c7cc.svg)](https://wakatime.com/badge/user/510092ca-a9b8-48f5-bf50-9b05005ef525/project/a5b9008a-d413-431f-92d4-80beef67c7cc)

The technologies being used are:
- [Python](https://www.python.org/) (Language)
- [Flask](https://flask.palletsprojects.com/en/2.1.x/) (Framework)
- [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) (Database)
- HTML/CSS/JS (Frontend)
- [Google Maps](https://www.google.com/maps) (Mapping)
- [Linode](https://www.linode.com/)/[Nginx](https://www.nginx.com/)/[Gunicorn](https://gunicorn.org/)/[Supervisord](http://supervisord.org/) (Server)

## Local App Installation (for local development)

Before running any scripts, make sure to check if you have Python installed on your machine. If you aren't sure, 
{download the latest version of Python](https://www.python.org/downloads/) and install it on your system.

If you are running Windows on your machine, it is also necessary to have Git Bash for Windows installed. 
If you don't have it already, please [download the latest version](https://git-scm.com/downloads) and install it on your system.

The easiest way to clone the repository is to use the HTTPS method. When inside of your preferred shell 
(Git Bash, Bash, zsh, ect), use the command ```git clone https://github.com/cmadajski/niner_miner.git``` 
and the files will be downloaded to your local system.

For more advanced users, SSH is an even better way to interact with GitHub repos. For detailed instructions 
on using SSH with GitHub, [check out this webpage.](https://docs.github.com/en/authentication/connecting-to-github-with-ssh) 
Use ```git@github.com:cmadajski/niner_miner.git``` to clone the repo via SSH.

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
In the even that you encounter a database error or you add new models to the database, it might be necessary to reset the databse.
To simplify this process, a script in the ```niner_miner/src/``` directory named reset_db.py automates the process of resetting the database.
To reset the database use the command ```python reset_db.py```

## Currently Implemented Features

- Login (with input validation)
- Password Reset (while not logged in)
- Password Reset (while logged in)
- Post New Items for Sale
- View All Items Posted by Current User
- Account Page for Current User
- Edit Account Info for Current User
- Delete Account for Current User
- View Detailed Item Information
