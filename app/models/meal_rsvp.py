from . import db
from datetime import date

class MealRSVP(db.Model):
    __tablename__ = 'meal_rsvps'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    
    # By default, we assume a student is eating unless they opt out
    eating_breakfast = db.Column(db.Boolean, default=True)
    eating_lunch = db.Column(db.Boolean, default=True)
    eating_snacks = db.Column(db.Boolean, default=True)
    eating_dinner = db.Column(db.Boolean, default=True)

    user = db.relationship('User', backref=db.backref('meal_rsvps', lazy='dynamic', cascade='all, delete-orphan'))

    # Ensure one RSVP per user per day
    __table_args__ = (db.UniqueConstraint('user_id', 'date', name='uq_user_date'),)
