import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import db
from app.models.user import User
from app.models.staff_profile import StaffProfile

app = create_app()

with app.app_context():
    staff_users = User.query.filter_by(role='staff').all()
    print("Staff in User table:", len(staff_users))
    for s in staff_users:
        print(f"User ID: {s.id}, Email: {s.email}")
        
    profiles = StaffProfile.query.all()
    print("\nStaff in StaffProfile table:", len(profiles))
    for p in profiles:
        print(f"Profile ID: {p.id}, User ID: {p.user_id}, Name: {p.full_name}")
