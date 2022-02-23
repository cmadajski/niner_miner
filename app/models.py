from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    phone = db.Column(db.String(10))
    validated = db.Column(db.Boolean)

    def __repr__(self):
        return f'<User {self.name}: {self.id}>'

    def __str__(self):
        return f'{self.name}: {self.email}'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100))
    user = db.Column(db.Integer)
    price = db.Column(db.Float)
    description = db.Column(db.String(200))
