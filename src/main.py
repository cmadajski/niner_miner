from unicodedata import category
from flask import Flask, flash, render_template, url_for, redirect, request
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
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(24), nullable=False)
    validation_code = db.Column(db.String(6), default=None)
    active = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return f'{self.name}({self.id})>> {self.email}'

    def is_active(self):
        return self.active


# have not added user logic yet to this
class Items(db.Model):
    item_id = db.Column("item_id", db.Integer, primary_key=True)
    title = db.Column("title", db.String(200))
    price = db.Column("price", db.Numeric, nullable=False)
    fixed = db.Column("fixed", db.Text)
    category = db.Column("category", db.Text)
    condition = db.Column("condition", db.Text)
    extradetails = db.Column("extradetails", db.Text)
    description = db.Column("description", db.String(1000))
    location = db.Column("location", db.Text)

    def __init__(self, title, price, fixed, category, condition, extradetails, description, location):
        self.title = title
        self.price = price
        self.fixed = fixed
        self.category = category
        self.condition = condition
        self.extradetails = extradetails
        self.description = description
        self.location = location


class sellItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.item_id'))


# index route is used for log in related functions
@app.route('/', methods=['GET', 'POST'])
def index():
    errors = dict()
    errors['email'] = False
    errors['password'] = False
    errors['email_str'] = ''
    errors['password_str'] = ''
    if request.method == 'GET':
        return render_template('index.html', errors=errors, info=None)
    elif request.method == 'POST':
        login_attempt = dict()
        login_attempt['email'] = request.form['email']
        login_attempt['password'] = request.form['password']

        # does email exist in the database?
        requested_user = User.query.filter_by(email=login_attempt['email']).first()
        if requested_user != None:
            # is the requested user activated?
            if requested_user.is_active() == False:
                errors['email'] = True
                errors['email_str'] = 'Account has not been validated yet!'
            # is password valid for the requested user?
            if requested_user.password != login_attempt['password']:
                errors['password'] = True
                errors['password_str'] = 'Password not valid for given email!'
        else:
            errors['email'] = True
            errors['email_str'] = 'Account does not exist for the given email!'
        if errors['email'] or errors['password']:
            return render_template('index.html', errors=errors, info=login_attempt)
        else:
            login_user(requested_user)
            flash('Successfully logged in as ' + current_user.name)
            return redirect('/product_feed')
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
            new_user = User(name=user_info['name'], id=user_info['id'], email=user_info['email'],
                            password=user_info['password'], validation_code=validation_code)
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

            gmail_password = 'Flaskapp4155!'
            # create secure SSL context
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, gmail_password)
                server.sendmail(sender_email, receiver_email, email_content)
            flash('A validation code has been sent to ' + user_info['email'])
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
            if requested_user.is_active() == True:
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
            requested_user.active = True
            db.session.commit()
            flash('Account for ' + requested_user.email + ' has been successfully activated!')
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
            if requested_user.is_active == True:
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
            flash('A new activation code has been sent to email ' + given_email)
            return redirect(url_for('validate'))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    errors = dict()
    errors['email'] = False
    errors['email_str'] = ''
    errors['id'] = False
    errors['id_str'] = ''
    errors['password'] = False
    errors['password_str'] = list()
    user_info = dict()
    if request.method == "GET":
        return render_template('forgot_password.html', errors=errors, user_info=None)
    elif request.method == "POST":
        user_info['email'] = request.form['email']
        user_info['id'] = (int)(request.form['id'])
        user_info['password'] = request.form['password']
        user_info['password_repeat'] = request.form['passwordRepeat']

        # does email exist in the database?
        requested_user = User.query.filter_by(email=user_info['email']).first()
        if requested_user == None:
            errors['email'] = True
            errors['email_str'] = 'No accounts exist for given email'
        else:
            # is id valid for the requested user?
            if requested_user.id != user_info['id']:
                errors['id'] = True
                errors['id_str'] = 'ID# not valid for given email!'

        # check if password is valid
        # is password at least 8 characters long?
        if len(user_info['password']) < 8:
            errors['password'] = True
            errors['password_str'].append('Password not 8+ characters long!')
        # do both passwords equal each other?
        if user_info['password'] != user_info['password_repeat']:
            errors['password'] = True
            errors['password_str'].append('Passwords do not match!')

        if errors['email'] or errors['id'] or errors['password']:
            return render_template('forgot_password.html', errors=errors, user_info=user_info)
        else:
            # update password for desired user
            requested_user.password = user_info['password']
            db.session.commit()
            flash('Password for ' + user_info['email'] + ' has been reset')
            return redirect(url_for('index'))
    else:
        return "HTTP REQUEST ERROR, CHECK BACKEND LOGIC"


@app.route('/product_feed')
@login_required
def product_feed():
    q = request.args.get('q')
    if q:
        posts = Items.query.filter(Items.title.contains(q) | Items.description.contains(q) | Items.category.contains(q) | Items.price.contains(q))
    # all_items = db.session.query(Items).all()
    else:
        posts = Items.query.all()
    return render_template('product_feed.html', items=posts, searched=q)


@app.route('/product_detail/<product_id>')
@login_required
def product_detail(product_id):
    item_details = Items.query.filter_by(item_id=product_id).first()
    return render_template('product_detail.html', item=item_details)


@app.route('/messages')
@login_required
def messages():
    return render_template('messages.html')


@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    if request.method == 'GET':
        return render_template('post.html', info=None)
    elif request.method == 'POST':
        # save form data into a dict for convenience
        item_info = dict()
        item_info['title'] = request.form['title']
        item_info['price'] = request.form['price']
        if 'submit_button' in request.form:
            item_info['fixed'] = request.form['fixed']
        if 'submit_button' in request.form:
            item_info['category'] = request.form['category']
        if 'submit_button' in request.form:
            item_info['condition'] = request.form['condition']
        item_info['extradetails'] = request.form['extradetails']
        item_info['description'] = request.form['description']
        if 'submit_button' in request.form:
            item_info['location'] = request.form['location']

        new_item = Items(title=item_info['title'], price=item_info['price'], fixed=item_info['fixed'],
                         category=item_info['category'], condition=item_info['condition'],
                         extradetails=item_info['extradetails'], description=item_info['description'],
                         location=item_info['location'])
        db.session.add(new_item)
        db.session.commit()

        return redirect(url_for('product_feed'))


@app.route('/my_items')
@login_required
def my_items():
    return render_template('my_items.html')


@app.route('/account')
@login_required
def account():
    return render_template('account.html')


@app.route('/account_edit')
@login_required
def account_edit():
    return render_template('account_edit.html')


@app.route('/account_delete')
@login_required
def account_delete():
    return render_template('account_delete.html')


@app.route('/account_reset_password', methods=['GET', 'POST'])
@login_required
def account_reset_password():
    errors = dict()
    errors['current_password'] = False
    errors['current_password_str'] = ''
    errors['new_password'] = False
    errors['new_password_str'] = list()
    if request.method == 'GET':
        return render_template('account_reset_password.html', errors=errors)
    elif request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        new_password_repeat = request.form['new_password_repeat']
        # check if password is valid
        # is current password valid for the current user?
        if current_password != current_user.password:
            errors['current_password'] = True
            errors['current_password_str'] = 'Password is not valid for current user!'
        # is password at least 8 characters long?
        if len(new_password) < 8:
            errors['new_password'] = True
            errors['new_password_str'].append('Password not 8+ characters long!')
        # do both passwords equal each other?
        if new_password != new_password_repeat:
            errors['new_password'] = True
            errors['new_password_str'].append('Passwords do not match!')
        # if errors exist, show them to user
        if errors['current_password'] or errors['new_password']:
            return render_template('account_reset_password.html', errors=errors)
        else:
            flash('Password successfully changed!')
            current_user.password = new_password
            db.session.commit()
            return redirect(url_for('account'))
    else:
        return "REQUEST ERROR, CHECK BACKEND CODE"


@app.route('/billing')
@login_required
def billing():
    return "BILLING AND PAYMENTS INFO GOES HERE"


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logged out.')
    return redirect('/')


if __name__ == '__main__':
    # run app normally
    app.run(debug=True)
    # allow phone access by running over a local network
    # app.run(debug=True, host='192.168.0.6')