from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy

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
    if request.method == 'GET':
        return render_template('signup.html', emailError=False, passwordError=False, emailMessage='', passwordMessage='')
    elif request.method == 'POST':
        emailError = False
        emailMessage = ''
        passwordError = False
        passwordMessage = ''
        # save form data into local variables
        email = request.form['email']
        password = request.form['password']
        password_repeat = request.form['passwordRepeat']
        name = request.form['name']
        id = request.form['id']
        phone = request.form['phone']

        # check if email is valid
        # does email include a UNCC address?
        if 'uncc.edu' not in email:
            emailError = True
            emailMessage += 'Not a UNCC email address!'

        # check if password is valid
        # is password at least 8 characters long?
        if len(password) < 8:
            passwordError = True
            passwordMessage += 'Password not 8+ characters long!'
        if password != password_repeat:
            passwordError = True
            # add newline if previous message exists
            if len(passwordMessage) > 0:
                passwordMessage += '<br>'
            passwordMessage += 'Passwords do not match!'
        if emailError or passwordError:
            return render_template('signup.html', emailError=emailError, passwordError=passwordError, emailMessage=emailMessage, passwordMessage=passwordMessage)
        else:
            return redirect(url_for('validate'))


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

if __name__ == '__main__':
    app.run()