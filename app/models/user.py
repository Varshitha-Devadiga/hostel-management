from . import db
from flask_login import UserMixin
from . import bcrypt


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin', 'student', 'staff', name='user_roles'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relationships (lazy='select' to avoid eager-load crashes)
    student = db.relationship('Student', backref='user', uselist=False, lazy='select', cascade='all, delete-orphan')
    # staff = db.relationship('Staff', backref='user', uselist=False, lazy='select')  # uncomment when Staff model exists

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
