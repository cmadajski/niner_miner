import email
from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from random import randint
import smtplib, ssl

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'most secret key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# database models
class User(db.Model):
    name = db.Column(db.String(50), nullable=False)
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    phone = db.Column(db.String(10))
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(24), nullable=False)
    validation_code = db.Column(db.String(6), default=None)
    validated = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'{self.name}({self.id})>> {self.email}'


# index route is used for log in related functions
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        return 'USING POST'
    else:
        return 'METHOD ERROR, CHECK BACKEND LOGIC'

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # data for input validation
    errors = dict()
    errors['email'] = False
    errors['password'] = False
    errors['email_str'] = ''
    errors['password_str'] = list()

    if request.method == 'GET':
        return render_template('signup.html', errors=errors)
    elif request.method == 'POST':
        
        # save form data into a dict for convenience
        user_info = dict()
        user_info['name'] = request.form['name']
        user_info['id'] = request.form['id']
        user_info['phone'] = request.form['phone']
        user_info['email'] = request.form['email']
        user_info['password'] = request.form['password']
        user_info['password_repeat'] = request.form['passwordRepeat']
        
        # check if email is valid
        # does email include a UNCC address?
        if 'uncc.edu' not in user_info['email']:
            errors['email'] = True
            errors['email_str'] = 'Not a UNCC email address!'
        # does the email already exist in the database?
        # ADD CODE HERE

        # check if password is valid
        # is password at least 8 characters long?
        if len(user_info['password']) < 8:
            errors['password'] = True
            errors['password_str'].append('Password not 8+ characters long!')
        # do both passwords equal each other?
        if user_info['password'] != user_info['password_repeat']:
            errors['password'] = True
            errors['password_str'].append('Passwords do not match!')
        # 
        if errors['email'] or errors['password']:
            return render_template('signup.html', errors=errors)
        else:
            # generate random 6 digit code
            validation_code = ''
            for i in range(6):
                num = randint(0, 9)
                validation_code += str(num)
            
            # add new user data to database
            new_user = User(name=user_info['name'], id=user_info['id'], phone=user_info['phone'], email=user_info['email'], password=user_info['password'], validation_code=validation_code)
            db.session.add(new_user)
            db.session.commit()
            
            # send email with validation code
            port = 465
            smtp_server = 'smtp.gmail.com'
            sender_email = 'ninerminer.alerts@gmail.com'
            receiver_email = user_info['email']
            email_content = f"""\
            SUBJECT: Your Validation Code for Niner Miner

            Hi there {user_info['name']},\n
            Here's the six-digit validation code for validating your new Niner Miner account.

            CODE:\t{validation_code}

            Visit 127.0.0.1:5000/validate to enter in your code.

            Have fun buying an selling!
            The Niner Miner Team
            """
            # read password from text file
            file = open('../password.txt', 'r')
            gmail_password = file.read()
            # create secure SSL context
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, gmail_password)
                server.sendmail(sender_email, receiver_email, email_content)

            return redirect(url_for('validate'))


@app.route('/validate')
def validate():
    if request.method == 'GET':
        return render_template('validate.html')
    elif request.method == 'POST':
        return 'NO LOGIC FOR POST REQUESTS YET'

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

if __name__ == '__main__':
    app.run()