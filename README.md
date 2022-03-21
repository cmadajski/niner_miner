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
For your convenience, we made a single script that creates a virtual environment, installs dependencies, 
and creates the database automatically. In the niner_miner directory, open the ```install``` directory. 
- if you are using Git Bash for Windows, use the command ```./app_install_windows_gitbash.sh```
- if you are using Mac(zsh) or Linux(bash, dash, etc), use the command ```./app_install_mac_linux.sh```

If you see any errors, then send us an email and we will work on fixing the problem. Otherwise, if you want 
to take the initiative yourself, just open the script file and use the commands one-by-one to set up the 
application yourself.

## Running the Code
Navigate to the ```src``` directory. Then use the command ```python main.py``` to start
the development server and allow access to the app.

An IP Address should be visible in the console, and you can either ctl+click the address
or copy and paste the address into a web browser to view the app. You can also manually
enter this address into your webbrowser if needed: ```http://127.0.0.1:5000/```

## Resetting the Database
While we are in the process of building and testing the application, it is sometimes necessary to delete and 
rebuild the database to remove existing data and start from scratch. To simplify this process, a script in the
```src/``` directory named reset_db.py automates the process of resetting the database. 

To reset the command the command ```python reset_db.py```

## Work in Progress
At this time in development, the application still has most of its functions non-operational.
We are hoping to have most functions working as intended by the last week of April.
