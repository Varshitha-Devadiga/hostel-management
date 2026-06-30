from . import db
from datetime import datetime


class LeaveRequest(db.Model):
    __tablename__ = 'leave_requests'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    leave_type = db.Column(db.String(50), nullable=False)  # e.g. 'casual', 'outpass', 'emergency'
    reason = db.Column(db.Text, nullable=False)
    from_date = db.Column(db.Date, nullable=False)
    to_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='Pending')  # Pending, Approved, Rejected
    is_returned = db.Column(db.Boolean, default=False)
    return_time = db.Column(db.String(10), nullable=True)
    return_notes = db.Column(db.Text, nullable=True)
    
    # New fields for Nursing Duty & College Fest
    shift_type = db.Column(db.String(50), nullable=True)  # Day Duty, Night Duty, General Duty
    expected_return_time = db.Column(db.String(10), nullable=True)
    attachment_path = db.Column(db.String(255), nullable=True)
    ocr_text = db.Column(db.Text, nullable=True)
    ocr_extracted_dates = db.Column(db.String(255), nullable=True)
    ocr_days = db.Column(db.Integer, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('leave_requests', lazy='dynamic', cascade='all, delete-orphan'))