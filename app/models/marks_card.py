from . import db
from datetime import datetime

class MarksCard(db.Model):
    __tablename__ = 'marks_cards'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default='Pending')  # Pending, Verified, Rejected
    extracted_cgpa = db.Column(db.String(10), nullable=True)
    admin_notes = db.Column(db.Text, nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('marks_cards', lazy='dynamic', cascade='all, delete-orphan'))

class MarksTimeline(db.Model):
    __tablename__ = 'marks_timeline'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status_type = db.Column(db.String(20), default='info')  # success, error, info, warning
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('marks_timeline', lazy='dynamic', order_by='MarksTimeline.created_at.desc()', cascade='all, delete-orphan'))
