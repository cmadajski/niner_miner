from unicodedata import category
from flask import Flask, flash, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from random import randint
import smtplib, ssl, copy
import os

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
    phone = db.Column(db.String(15), default=None)
    password = db.Column(db.String(24), nullable=False)
    validation_code = db.Column(db.String(6), default=None)
    active = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return f'{self.name}({self.id})>> {self.email}'

    def is_active(self):
        return self.active



class Items(db.Model):
    item_id = db.Column("item_id", db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column("title", db.String(200))
    price = db.Column("price", db.Numeric, nullable=False)
    fixed = db.Column("fixed", db.Text)
    category = db.Column("category", db.Text)
    condition = db.Column("condition", db.Text)
    extradetails = db.Column("extradetails", db.Text)
    description = db.Column("description", db.String(1000))
    location = db.Column("location", db.Text)

    def __init__(self, seller_id, title, price, fixed, category, condition, extradetails, description, location):
        self.seller_id = seller_id
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
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    seller_name = db.Column(db.String(50), db.ForeignKey('user.name'))
    seller_email = db.Column(db.String(40), db.ForeignKey('user.email'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.item_id'))
    buyer_id = db.Column(db.Integer, default=None)

    def __init__(self, seller_id, seller_name, seller_email, item_id, buyer_id):
        self.seller_id = seller_id
        self.seller_name = seller_name
        self.seller_email = seller_email
        self.item_id = item_id
        self.buyer_id = buyer_id

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
        user_info['phone'] = request.form['phone']
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
                            phone=user_info['phone'], password=user_info['password'], validation_code=validation_code)
            db.session.add(new_user)
            db.session.commit()

            # add new directory for saving user account img
            try:
                path = './static/img/accounts/' + (str)(user_info['id'])
                os.makedirs(path)
            except FileExistsError:
                print("OS_ERROR - Directory already exists!")

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
    f = request.args.get('f')
    print(f)
    print(type(f))
    if f == "All" or f == None:
        print("at all")
        if q:
            posts = Items.query.filter(Items.title.contains(q) | Items.description.contains(q) | Items.category.contains(q) | Items.price.contains(q))
        # all_items = db.session.query(Items).all()
        else:
            posts = Items.query.all()
        return render_template('product_feed.html', items=posts, searched=q, filtered=f, user=current_user)
    else:
        print("at else")
        if q:
            posts = Items.query.filter(Items.category.contains(f) & (Items.title.contains(q) | Items.description.contains(q) | Items.category.contains(q) | Items.price.contains(q)))
        # all_items = db.session.query(Items).all()
        else:
            posts = Items.query.filter(Items.category.is_(f))
        return render_template('product_feed.html', items=posts, searched=q, filtered=f, user=current_user)


@app.route('/product_detail/<product_id>')
@login_required
def product_detail(product_id):
    item_details = Items.query.filter_by(item_id=product_id).first()
    selling_info = sellItem.query.filter_by(item_id=product_id).first()
    return render_template('product_detail.html', item=item_details, user=current_user, seller=selling_info)

# CURRENTLY WORKING ON THIS BRANCH!
@app.route('/edit/<product_id>', methods=['GET', 'POST'])
@login_required
def edit_item(product_id):
    # data for input validation
    errors = dict()
    errors['title'] = False
    errors['price'] = False
    errors['image'] = False
    errors['fixed'] = False
    errors['category'] = False
    errors['condition'] = False
    errors['description'] = False
    errors['location'] = False
    errors['title_str'] = ''
    errors['price_str'] = ''
    errors['image_str'] = ''
    errors['fixed_str'] = ''
    errors['category_str'] = ''
    errors['condition_str'] = ''
    errors['description_str'] = ''
    errors['location_str'] = ''

    if request.method == 'POST':
        item_info = dict()
        item_info['title'] = request.form['title']
        item_info['price'] = request.form['price']
        item_info['fixed'] = request.form['fixed']
        item_info['category'] = request.form['category']
        item_info['condition'] = request.form['condition']
        item_info['extradetails'] = request.form['extradetails']
        item_info['description'] = request.form['description']
        item_info['location'] = request.form['location']

         # this section of if statements cover input validation for the post form
        if len(item_info['title']) <= 1:
            errors['title'] = True
            errors['title_str'] = 'Please enter a proper title to post.'
        
        if item_info['price'] == '':
            errors['price'] = True
            errors['price_str'] = 'Please enter a price.'
        
        if item_info['fixed'] == None:
            errors['fixed'] = True
            errors['fixed_str'] = 'Please select an option for this category.'
        
        if item_info['category'] == None:
            errors['category'] = True
            errors['category_str'] = 'Please select an option for this category.'

        if item_info['condition'] == None:
            errors['condition'] = True
            errors['condition_str'] = 'Please select an option for this category.'
        
        if item_info['description'] == '':
            errors['description'] = True
            errors['description_str'] = 'Please include a description.'
        
        if item_info['location'] == None:
            errors['location'] = True
            errors['location_str'] = 'Please select a location below.'
        
        # if there are errors in the form, print these errors in post.html
        if errors['title'] or errors['price'] or errors['fixed'] or errors['category'] or errors['condition'] or errors['description'] or errors['location']:
            return render_template('post.html', errors=errors, info=item_info)
        else:
            #find the item you want to edit
            item = Items.query.filter_by(item_id=product_id).first()

            # update the fields in post
            item.title = item_info['title']
            item.price = item_info['price']
            item.fixed = item_info['fixed']
            item.category = item_info['category']
            item.condition = item_info['condition']
            item.extradetails = item_info['extradetails']
            item.description = item_info['description']
            item.location = item_info['location']

            # update item in database
            db.session.add(item)
            db.session.commit()

            img1 = request.files['image1']
            if img1.filename == '':
                # if no image is uploaded, you will receive an error message
                errors['image'] = True
                errors['image_str'] = 'You are required to upload 5 images.'

                if errors['image']:
                    return render_template('post.html', errors=errors, info=item_info)
            else:
                # define the path used for item images
                filename = (str)(item.item_id) + 'image1'
                path = './static/img/accounts/' + (str)(current_user.id) + '/' + filename
                #old_path = '../static/img/empty.jpg'
                # remove the old item img
                #os.remove(path)
                # save the new img
                img1.save(path)

            img2 = request.files['image2']
            if img2.filename == '':
                errors['image'] = True
                errors['image_str'] = 'You are required to upload 5 images.'

                if errors['image']:
                    return render_template('post.html', errors=errors, info=item_info)
            else:
                # define the path used for item images
                filename = (str)(item.item_id) + 'image2'
                path = './static/img/accounts/' + (str)(current_user.id) + '/' + filename
                #old_path = '../static/img/empty.jpg'
                # remove the old item img
                #os.remove(path)
                # save the new img
                img2.save(path)
            
            img3 = request.files['image3']
            if img3.filename == '':
                errors['image'] = True
                errors['image_str'] = 'You are required to upload 5 images.'

                if errors['image']:
                    return render_template('post.html', errors=errors, info=item_info)
            else:
                # define the path used for item images
                filename = (str)(item.item_id) + 'image3'
                path = './static/img/accounts/' + (str)(current_user.id) + '/' + filename
                #old_path = '../static/img/empty.jpg'
                # remove the old item img
                #os.remove(path)
                # save the new img
                img3.save(path)

            img4 = request.files['image4']
            if img4.filename == '':
                errors['image'] = True
                errors['image_str'] = 'You are required to upload 5 images.'

                if errors['image']:
                    return render_template('post.html', errors=errors, info=item_info)
            else:
                # define the path used for item images
                filename = (str)(item.item_id) + 'image4'
                path = './static/img/accounts/' + (str)(current_user.id) + '/' + filename
                #old_path = '../static/img/empty.jpg'
                # remove the old item img
                #os.remove(path)
                # save the new img
                img4.save(path)

            img5 = request.files['image5']
            if img5.filename == '':
                errors['image'] = True
                errors['image_str'] = 'You are required to upload 5 images.'

                if errors['image']:
                    return render_template('post.html', errors=errors, info=item_info)
            else:
                # define the path used for item images
                filename = (str)(item.item_id) + 'image5'
                path = './static/img/accounts/' + (str)(current_user.id) + '/' + filename
                #old_path = '../static/img/empty.jpg'
                # remove the old item img
                #os.remove(path)
                # save the new img
                img5.save(path)

            # return to product feed page            
            return redirect(url_for('product_feed'))
    else:
        # GET request - show new post form to edit the item details
        # retrieve item from database
        my_item = Items.query.filter_by(item_id=product_id).first()

        return render_template('post.html', errors=errors, item=my_item, user=current_user, info=my_item)

@app.route('/delete/<product_id>', methods=['POST'])
@login_required
def delete_item(product_id):
    # retrieve item from database
    my_item = Items.query.filter_by(item_id=product_id).first()

    db.session.delete(my_item)
    db.session.commit()

    # return to product feed page            
    return redirect(url_for('product_feed'))

@app.route('/messages')
@login_required
def messages():
    return render_template('messages.html')


@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
     # data for input validation
    errors = dict()
    errors['title'] = False
    errors['price'] = False
    errors['image'] = False
    errors['fixed'] = False
    errors['category'] = False
    errors['condition'] = False
    errors['description'] = False
    errors['location'] = False
    errors['title_str'] = ''
    errors['price_str'] = ''
    errors['image_str'] = ''
    errors['fixed_str'] = ''
    errors['category_str'] = ''
    errors['condition_str'] = ''
    errors['description_str'] = ''
    errors['location_str'] = ''


    if request.method == 'GET':
        return render_template('post.html', errors=errors, info=None)
    elif request.method == 'POST':
        # save form data into a dict for convenience
        item_info = dict()
        item_info['title'] = request.form['title']
        item_info['price'] = request.form['price']
        # if 'submit_button' in request.form:
        item_info['fixed'] = request.form['fixed']
        # if 'submit_button' in request.form:
        item_info['category'] = request.form['category']
        # if 'submit_button' in request.form:
        item_info['condition'] = request.form['condition']
        item_info['extradetails'] = request.form['extradetails']
        item_info['description'] = request.form['description']
        # if 'submit_button' in request.form:
        item_info['location'] = request.form['location']

        # this section of if statements cover input validation for the post form
        if len(item_info['title']) <= 1:
            errors['title'] = True
            errors['title_str'] = 'Please enter a proper title to post.'
        
        if item_info['price'] == '':
            errors['price'] = True
            errors['price_str'] = 'Please enter a price.'
        
        if item_info['fixed'] == None:
            errors['fixed'] = True
            errors['fixed_str'] = 'Please select an option for this category.'
        
        if item_info['category'] == None:
            errors['category'] = True
            errors['category_str'] = 'Please select an option for this category.'

        if item_info['condition'] == None:
            errors['condition'] = True
            errors['condition_str'] = 'Please select an option for this category.'
        
        if item_info['description'] == '':
            errors['description'] = True
            errors['description_str'] = 'Please include a description.'
        
        if item_info['location'] == None:
            errors['location'] = True
            errors['location_str'] = 'Please select a location below.'
        
        # if there are errors in the form, print these errors in post.html
        if errors['title'] or errors['price'] or errors['fixed'] or errors['category'] or errors['condition'] or errors['description'] or errors['location']:
            return render_template('post.html', errors=errors, info=item_info)
        else:
        # else add the item to the database
            new_item = Items(seller_id=current_user.id, title=item_info['title'], price=item_info['price'], fixed=item_info['fixed'],
                            category=item_info['category'], condition=item_info['condition'],
                            extradetails=item_info['extradetails'], description=item_info['description'],
                            location=item_info['location'])
            db.session.add(new_item)
            db.session.commit()

            selling_item = sellItem(seller_id=current_user.id, seller_name=current_user.name, seller_email=current_user.email, item_id=new_item.item_id, buyer_id=None)
            db.session.add(selling_item)
            db.session.commit()

            new_img1 = request.files['image1']
            if new_img1.filename == '':
                # if no image is uploaded, you will receive an error message
                errors['image'] = True
                errors['image_str'] = 'You are required to upload 5 images.'

                if errors['image']:
                    return render_template('post.html', errors=errors, info=item_info)
            else:
                # define the path used for item images
                filename = (str)(new_item.item_id) + 'image1'
                path = './static/img/accounts/' + (str)(current_user.id) + '/' + filename
                #old_path = '../static/img/empty.jpg'
                # remove the old item img
                #os.remove(old_path)
                # save the new img
                new_img1.save(path)

            new_img2 = request.files['image2']
            if new_img2.filename == '':
                errors['image'] = True
                errors['image_str'] = 'You are required to upload 5 images.'

                if errors['image']:
                    return render_template('post.html', errors=errors, info=item_info)
            else:
                # define the path used for item images
                filename = (str)(new_item.item_id) + 'image2'
                path = './static/img/accounts/' + (str)(current_user.id) + '/' + filename
                #old_path = '../static/img/empty.jpg'
                # remove the old item img
                #os.remove(old_path)
                # save the new img
                new_img2.save(path)
            
            new_img3 = request.files['image3']
            if new_img3.filename == '':
                errors['image'] = True
                errors['image_str'] = 'You are required to upload 5 images.'

                if errors['image']:
                    return render_template('post.html', errors=errors, info=item_info)
            else:
                # define the path used for item images
                filename = (str)(new_item.item_id) + 'image3'
                path = './static/img/accounts/' + (str)(current_user.id) + '/' + filename
                #old_path = '../static/img/empty.jpg'
                # remove the old item img
                #os.remove(old_path)
                # save the new img
                new_img3.save(path)

            new_img4 = request.files['image4']
            if new_img4.filename == '':
                errors['image'] = True
                errors['image_str'] = 'You are required to upload 5 images.'

                if errors['image']:
                    return render_template('post.html', errors=errors, info=item_info)
            else:
                # define the path used for item images
                filename = (str)(new_item.item_id) + 'image4'
                path = './static/img/accounts/' + (str)(current_user.id) + '/' + filename
                #old_path = '../static/img/empty.jpg'
                # remove the old item img
                #os.remove(old_path)
                # save the new img
                new_img4.save(path)

            new_img5 = request.files['image5']
            if new_img5.filename == '':
                errors['image'] = True
                errors['image_str'] = 'You are required to upload 5 images.'

                if errors['image']:
                    return render_template('post.html', errors=errors, info=item_info)
            else:
                # define the path used for item images
                filename = (str)(new_item.item_id) + 'image5'
                path = './static/img/accounts/' + (str)(current_user.id) + '/' + filename
                #old_path = '../static/img/empty.jpg'
                # remove the old item img
                #os.remove(old_path)
                # save the new img
                new_img5.save(path)
            # return to product feed page
            return redirect(url_for('product_feed'))


@app.route('/my_items')
@login_required
def my_items():
    #pass in all the items in the Items table
    posts = Items.query.all()
    return render_template('my_items.html', items=posts, user=current_user)


@app.route('/account')
@login_required
def account():
    return render_template('account.html', user=current_user)

@app.route('/account_change_img')
@login_required
def account_change_img():
    return render_template('account_change_img.html')

@app.route('/upload_img', methods=['POST'])
@login_required
def upload_img():
    new_img = request.files['new_img']
    if new_img.filename == '':
        flash('No file selected for upload!')
    else:
        # define the path used for account images
        filename = 'account_img'
        path = './static/img/accounts/' + (str)(current_user.id) + '/' + filename
        # remove the old account img
        os.remove(path)
        # save the new img
        new_img.save(path)
        # return to account page
        return redirect('/account')


@app.route('/account_edit')
@login_required
def account_edit():
    return render_template('account_edit.html', user=current_user)

@app.route('/account_update', methods=['POST'])
@login_required
def account_update():

    current_user.name = request.form['name']
    current_user.phone = request.form['phone']
    db.session.commit()

    new_img = request.files['image']
    if new_img.filename != '':
        #flash('No file selected for upload!')

        # define the path used for account images
        filename = 'account_img'
        path = './static/img/accounts/' + (str)(current_user.id) + '/' + filename
        # remove the old account img
        os.remove(path)
        # save the new img
        new_img.save(path)
        # return to account page

    flash('Your profile has been successfully updated')
    return redirect('/account')

@app.route('/account_delete')

@app.route('/account_delete', methods=['GET', 'POST'])
@login_required
def account_delete():
    errors = dict()
    errors['current_password'] = False
    errors['current_password_str'] = ''
    if request.method == 'GET':
        return render_template('account_delete.html', errors=errors)
    elif request.method == 'POST':
        current_password = request.form['current_password']
        # check if password is valid
        # is current password valid for the current user?
        if current_password != current_user.password:
            errors['current_password'] = True
            errors['current_password_str'] = 'Password is not valid for current user!'
        # if errors exist, show them to user
        if errors['current_password']:
            return render_template('account_delete.html', errors=errors)
        else:
            flash('Your account has been successfully deleted!')
            #delete user account code goes here

            #logout after account deleted
            return redirect(url_for('logout'))
    else:
        return "REQUEST ERROR, CHECK BACKEND CODE"


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