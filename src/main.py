import re
from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from random import randint
import smtplib, ssl, copy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'most secret key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# flask login stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

# database models
class User(db.Model, UserMixin):
    name = db.Column(db.String(50), nullable=False)
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    phone = db.Column(db.String(10))
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(24), nullable=False)
    validation_code = db.Column(db.String(6), default=None)
    is_validated = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'{self.name}({self.id})>> {self.email}'


# index route is used for log in related functions
@app.route('/', methods=['GET', 'POST'])
def index():
    errors = dict()
    errors['email'] = False
    errors['password'] = False
    errors['email_str'] = ''
    errors['password_str'] = ''
    if request.method == 'GET':
        return render_template('index.html', errors=errors, user_info=None)
    elif request.method == 'POST':
        login_attempt = dict()
        login_attempt['email'] = request.form['email']
        login_attempt['password'] = request.form['password']
        
        # does email exist in the database?
        requested_user = User.query.filter_by(email=login_attempt['email']).first()
        if requested_user != None:
            # is password valid for the requested user?
            if requested_user.password == login_attempt['password']:
                login_user(requested_user)
                return redirect('/product_feed')
            else:
                errors['password'] = True
                errors['password_str'] = 'Password not valid for given email!'
        else:
            errors['email'] = True
            errors['email_str'] = 'Account does not exist for the given email!'
        if errors['email'] or errors['password']:
            return render_template('index.html', errors=errors, user_info=login_attempt)
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
        return render_template('signup.html', errors=errors, info=None)
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
        requested_user = User.query.filter_by(email=user_info['email']).first()
        if requested_user != None:
            errors['email'] = True
            errors['email_str'] = 'Email address is already associated with an account!'

        # check if password is valid
        # is password at least 8 characters long?
        if len(user_info['password']) < 8:
            errors['password'] = True
            errors['password_str'].append('Password not 8+ characters long!')
        # do both passwords equal each other?
        if user_info['password'] != user_info['password_repeat']:
            errors['password'] = True
            errors['password_str'].append('Passwords do not match!')
        # if errors exist, show them to user
        if errors['email'] or errors['password']:
            return render_template('signup.html', errors=errors, info=user_info)
        # if no errors exist, then add user to database and email verification code
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

            CODE: {validation_code}

            Visit 127.0.0.1:5000/validate to enter in your code.

            Have fun buying an selling!
            The Niner Miner Team
            """
            
            gmail_password = 'Ninerminer1234!'
            # create secure SSL context
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, gmail_password)
                server.sendmail(sender_email, receiver_email, email_content)

            return redirect(url_for('validate'))


@app.route('/validate', methods=['GET', 'POST'])
def validate():
    # data for input validation
    errors = dict()
    errors['email'] = False
    errors['code'] = False
    errors['email_str'] = ''
    errors['code_str'] = ''

    if request.method == 'GET':
        return render_template('validate.html', errors=errors)
    elif request.method == 'POST':
        given_email = request.form['email']
        given_code = request.form['code']

        # is email already in the system?
        requested_user = User.query.filter_by(email=given_email).first()
        if requested_user == None:
            errors['email'] = True
            errors['email_str'] = 'No account associated with given email address'
        
        # is account already validated?
        else:
            if requested_user.is_validated == True:
                errors['email'] = True
                errors['email_str'] = f'Account with email {given_email} is already validated!'
            
            # is the code valid for the requested user?
            if given_code != requested_user.validation_code:
                errors['code'] = True
                errors['code_str'] = 'Code not valid, try again or resend another code.'

        if errors['email'] or errors['code']:
            return render_template('validate.html', errors=errors)
        else:
            # change account validation status to true
            requested_user.is_validated = True
            db.session.commit()
            return redirect(url_for('index'))

@app.route('/resend_validation', methods=['GET', 'POST'])
def resend_validation():
    errors = dict()
    errors['email'] = False
    errors['email_str'] = ''
    if request.method == 'GET':
        return render_template('resend_validation.html', errors=errors)
    elif request.method == 'POST':
        given_email = request.form['email']

        # is email already in the system?
        requested_user = User.query.filter_by(email=given_email).first()
        if requested_user == None:
            errors['email'] = True
            errors['email_str'] = 'No account associated with given email address'
        # is account already validated?
        else:
            if requested_user.is_validated == True:
                errors['email'] = True
                errors['email_str'] = f'Account with email {given_email} is already validated!'
        # if errors are found, show errors to user
        if errors['email']:
            return render_template('resend_validation.html', errors=errors)
        # if no errors are found, resend the verification code
        else:
            # generate new 6-digit verification code
            validation_code = ''
            for i in range(6):
                num = randint(0, 9)
                validation_code += str(num)
            # assign user with new code
            requested_user.validation_code = validation_code
            db.session.commit()
            # add code for sending new email here
            port = 465
            smtp_server = 'smtp.gmail.com'
            sender_email = 'ninerminer.alerts@gmail.com'
            receiver_email = requested_user.email
            email_content = f"""\
            SUBJECT: Your Validation Code for Niner Miner

            Hi there {requested_user.name},\n
            Here's the six-digit validation code for validating your new Niner Miner account.

            CODE:\t{validation_code}

            Visit 127.0.0.1:5000/validate to enter in your code.

            Have fun buying an selling!
            The Niner Miner Team
            """
            # read password from text file (for security)
            gmail_password = 'Ninerminer1234!'
            # create secure SSL context
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                # login to server
                server.login(sender_email, gmail_password)
                # send email to user
                server.sendmail(sender_email, receiver_email, email_content)
            return redirect(url_for('validate'))

@app.route('/about')
def about():
    return "ABOUT GOES HERE"

@app.route('/forgot_password')
@login_required
def forgot_password():
    return "FORGOT PASSWORD GOES HERE"

@app.route('/product_feed')
@login_required
def product_feed():
    return render_template('product_feed.html')

@app.route('/product_detail')
def product_detail():
    return 'SHOW DETAILED INFO FOR A SINGLE ITEM'

@app.route('/product_search')
def product_search():
    return 'SHOW ITEM FEED BASED ON USER SEARCH CRITERIA'

@app.route('/messages')
def messages():
    return render_template('messages.html')

@app.route('/post')
def post():
    return render_template('post.html')

@app.route('/my_items')
def my_items():
    return render_template('my_items.html')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/account_edit')
def account_edit():
    return 'EDIT ACCOUNT'

@app.route('/account_delete')
def account_delete():
    return 'DELETE ACCOUNT'

@app.route('/change_password')
def change_password():
    return 'CHANGE PASSWORD HERE'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

if __name__ == '__main__':
    app.run()