import os, sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# By is used for finding web elements of specific types (id, class_name, name, etc)
from selenium.webdriver.common.by import By
# Keys are used to simulate individual key presses on the keyboard instead of whole values
from selenium.webdriver.common.keys import Keys
# Termcolor adds colored text to terminal output
from termcolor import colored, cprint

# set up color printing for easier visual identification
# source: https://towardsdatascience.com/prettify-your-terminal-text-with-termcolor-and-pyfiglet-880de83fda6b
print_red = lambda x: cprint(x, 'red')
print_green = lambda x: cprint(x, 'green')
print_cyan = lambda x: cprint(x, 'cyan')

# set up test values (emails and passwords)
logins = list()
logins.append({'email': 'demo@uncc.edu', 'password':'demo1234'})
logins.append({'email': 'cmadajsk@uncc.edu', 'password': 'password2'})
logins.append({'email': 'random@uncc.edu', 'password': 'random1234'})
logins.append({'email': 'hmakadi1@uncc.edu', 'password': 'Niner@123'})

# set up test performance tracking
num_tests = len(logins)
num_passed: int = 0

# create a new webdriver instance
service = Service("C:/Users/Default.LAPTOP-TIFN37GP/Code/niner_miner/test/selenium_webdrivers/chromedriver.exe")
driver = webdriver.Chrome(service=service)
# access the deployed niner miner login page
# driver.get('http://194.195.214.161')

try:
    # access the development niner miner login page
    url = 'http://127.0.0.1:5000/'
    driver.get(url)
except:
    print_red(f'ERROR: Cannot connect to URL ({url})')
    driver.quit()
    quit()

# use loop to test multiple login attempts with different values in each case
for login in logins:
    # find email input field
    email = driver.find_element(By.NAME, 'email')
    # click on email input field
    email.click()
    # make sure the text field is empty
    email.clear()
    # change email value to a valid account email
    email.send_keys(login['email'])
    # find password input field
    password = driver.find_element(By.NAME, 'password')
    # click on password input field
    password.click()
    # make sure the text field is empty 
    password.clear()
    # change password value to a valid account password
    password.send_keys(login['password'])
    # find submit button for login form
    submit = driver.find_element(By.ID, 'submit')
    # click on submit button to progress to buy page
    submit.click()
    # the flash message that follows a successful login attempt will be
    # used as the signal for login success
    try:
        flash = driver.find_element(By.CLASS_NAME, 'flash')
        print_green(f"SUCCESS: login using {login['email']} account")
        num_passed += 1
        # find the logout link
        logout = driver.find_element(By.ID, 'logout')
        # click on the logout link to return to 
        logout.click()
    except:
        print_red(f"FAILED: login using {login['email']} account")

# calculate test performance
percentage = num_passed / num_tests
# format the performance test string
performance = '\nPERFORMANCE: {passed} out of {tests} tests passed ({perc:.2f}%).\n'.format(passed=num_passed, tests=num_tests, perc=percentage)
print_cyan(performance)
# close the browser instance
driver.quit()