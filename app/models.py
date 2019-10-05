from app import db, login

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    text = db.Column(db.String(5000), nullable=True)
    full_text = db.Column(db.String(5000), nullable=True)
    departure_date = db.Column(db.DateTime, nullable=True)
    receive_date = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Invoice {}>'.format(self.body)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String, unique=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))

    def __repr__(self):
        return str(self.invoice)