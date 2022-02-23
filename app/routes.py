from flask import Flask, render_template, url_for, redirect
from app import app
from app.models import User, Product



@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/logout')
def logout():
    return 'User logged out'


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/about')
def about():
    return render_template('about.html')


