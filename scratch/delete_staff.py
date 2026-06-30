import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import db
from app.models.user import User
from app.models.staff_profile import StaffProfile

app = create_app()

with app.app_context():
    # Find Pavithra
    user = User.query.filter_by(email='pavithra@gmail.com').first()
    if user:
        # Delete profile
        profile = StaffProfile.query.filter_by(user_id=user.id).first()
        if profile:
            db.session.delete(profile)
        
        # Delete user
        db.session.delete(user)
        db.session.commit()
        print(f"Deleted user pavithra@gmail.com and their profile.")
    else:
        print("pavithra@gmail.com not found.")
        
    # Also delete the other test staff just in case
    user2 = User.query.filter_by(email='staff@bcwd.in').first()
    if user2:
        profile2 = StaffProfile.query.filter_by(user_id=user2.id).first()
        if profile2:
            db.session.delete(profile2)
        db.session.delete(user2)
        db.session.commit()
        print(f"Deleted user staff@bcwd.in and their profile.")
