from flask_login import UserMixin
from extensions import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    jobs = db.relationship(
        'JobApplication',
        backref='user',
        lazy=True
    )



class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    color = db.Column(db.String(20), default='secondary')



class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    address = db.Column(db.String(200))
    applied_date = db.Column(db.DateTime)

    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    status = db.relationship('Status')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))





