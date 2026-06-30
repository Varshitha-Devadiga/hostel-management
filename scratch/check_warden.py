import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import db
from app.models.user import User

app = create_app()

with app.app_context():
    admins = User.query.filter_by(role='admin').all()
    print("Admin users in database:")
    for admin in admins:
        print(f"- ID: {admin.id}, Email: {admin.email}")
    
    specific_user = User.query.filter_by(email='Warden1@gmail.com').first()
    if specific_user:
        print(f"\nUser Warden1@gmail.com found. Role: {specific_user.role}")
        print(f"Password Check for 'padil@123': {specific_user.check_password('padil@123')}")
    else:
        print("\nUser Warden1@gmail.com NOT FOUND in the database.")
