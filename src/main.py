from flask import Flask, render_template, url_for, redirect

app = Flask(__name__)

# index route is used for log in related functions
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return "SIGN UP GOES HERE"

@app.route('/validate')
def validate():
    return 'CODE TO VALIDATE NEW ACCOUNT'

@app.route('/about')
def about():
    return "ABOUT GOES HERE"

@app.route('/forgot_password')
def forgot_password():
    return "FORGOT PASSWORD GOES HERE"

@app.route('/product_feed')
def product_feed():
    return 'SHOW LIST OF ALL PRODUCTS FOR SALE HERE'

@app.route('/product_detail')
def product_detail():
    return 'SHOW DETAILED INFO FOR A SINGLE ITEM'

@app.route('/product_search')
def product_search():
    return 'SHOW ITEM FEED BASED ON USER SEARCH CRITERIA'

@app.route('/messages')
def messages():
    return 'MESSAGES GO HERE'

@app.route('/post')
def post():
    return 'POST A NEW ITEM FOR SALE'

@app.route('/my_items')
def my_items():
    return 'SHOW LIST OF ALL CURRENT USERS ITEMS'

@app.route('/account')
def account():
    return 'ACCOUNT MAIN PAGE'

@app.route('/account_edit')
def account_edit():
    return 'EDIT ACCOUNT'

@app.route('/account_delete')
def account_delete():
    return 'DELETE ACCOUNT'

@app.route('/change_password')
def change_password():
    return 'CHANGE PASSWORD HERE'
