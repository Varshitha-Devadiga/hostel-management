from . import db
from .room import Room

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=True)  # optional room assignment
    dob = db.Column(db.Date)
    gender = db.Column(db.Enum('M', 'F', 'O', name='gender_enum'), default='O')
    food_pref = db.Column(db.Enum('veg', 'egg', 'chicken', 'fish', name='food_pref_enum'), default='veg')

    # relationships
    # room relationship (requires Room model)
    room = db.relationship('Room', backref='students', lazy='select', foreign_keys=[room_id])
     # leave_requests = db.relationship('LeaveRequest', backref='student', lazy='dynamic')
    # complaints = db.relationship('Complaint', backref='student', lazy='dynamic')
    # meal_responses = db.relationship('MealResponse', backref='student', lazy='dynamic')
