from . import db
from datetime import datetime

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False) # Hostel, Scholarship, Meeting, Holiday
    priority = db.Column(db.String(20), default='Normal') # Normal, High
    action_link = db.Column(db.String(255), nullable=True)
    action_text = db.Column(db.String(50), nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    target_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    target_role = db.Column(db.String(20), nullable=True)

    target_user = db.relationship('User', backref=db.backref('notifications', lazy=True))
