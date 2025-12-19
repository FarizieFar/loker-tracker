



from flask_login import UserMixin
from extensions import db
from datetime import datetime as dt

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    jobs = db.relationship(
        'JobApplication',
        backref='user',
        lazy=True
    )
    
    notifications = db.relationship(
        'Notification',
        backref='user',
        lazy=True
    )

class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    color = db.Column(db.String(20), default='secondary')

    jobs = db.relationship(
        'JobApplication',
        backref='status',
        lazy=True
    )

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100))
    position = db.Column(db.String(100), nullable=True)  # NEW: Posisi yang dilamar
    location = db.Column(db.String(100))
    address = db.Column(db.String(200))

    application_proof = db.Column(db.Text, nullable=True)  # NEW: Link atau path screenshot
    image_proof = db.Column(db.String(255), nullable=True)  # NEW: Path to uploaded image
    source_info = db.Column(db.String(100), nullable=True)  # NEW: Asal info loker
    logo_url = db.Column(db.String(255), nullable=True)  # NEW: URL logo perusahaan
    notes = db.Column(db.Text, nullable=True)  # NEW: Keterangan tambahan
    applied_date = db.Column(db.DateTime)


    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(20), default='info')  # info, success, warning, danger
    is_read = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=dt.utcnow)
    
    # Link to related job if applicable
    job_id = db.Column(db.Integer, db.ForeignKey('job_application.id'), nullable=True)





