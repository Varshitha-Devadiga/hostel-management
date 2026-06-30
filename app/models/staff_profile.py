from . import db
from datetime import datetime

class StaffProfile(db.Model):
    __tablename__ = 'staff_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    specialty = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    address = db.Column(db.Text, nullable=True)
    marital_status = db.Column(db.String(50), nullable=True)
    joined_date = db.Column(db.Date, default=datetime.utcnow)
    status = db.Column(db.String(20), default='On Duty') # On Duty, On Leave
    photo_path = db.Column(db.String(200), nullable=True)
    
    aadhaar_path = db.Column(db.String(200), nullable=True)
    ration_card_path = db.Column(db.String(200), nullable=True)
    aadhaar_verified = db.Column(db.Boolean, default=False)
    ration_verified = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref=db.backref('staff_profile', uselist=False, cascade='all, delete-orphan'))
