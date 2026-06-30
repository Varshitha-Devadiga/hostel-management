from . import db
from datetime import datetime

class FoodMenu(db.Model):
    __tablename__ = 'food_menu'

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(20), nullable=False, unique=True) # Monday, Tuesday, etc.
    breakfast = db.Column(db.String(200))
    lunch = db.Column(db.String(200))
    snacks = db.Column(db.String(200))
    dinner = db.Column(db.String(200))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
