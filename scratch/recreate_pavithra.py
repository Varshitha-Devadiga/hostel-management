import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import db
from app.models.user import User
from app.models.staff_profile import StaffProfile

app = create_app()

with app.app_context():
    email = 'pavithra@gmail.com'
    existing = User.query.filter_by(email=email).first()
    if not existing:
        new_user = User(email=email, role='staff')
        new_user.set_password('padil@123')
        db.session.add(new_user)
        db.session.flush() # get ID
        
        sp = StaffProfile(user_id=new_user.id, full_name='Pavithra', specialty='Kitchen Management')
        db.session.add(sp)
        db.session.commit()
        print(f"Recreated user {email} with password 'padil@123'")
    else:
        print(f"User {email} already exists.")
