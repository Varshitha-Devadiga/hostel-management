import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import db
from app.models.user import User
from app.models.staff_profile import StaffProfile

app = create_app()

with app.app_context():
    warden = User.query.filter_by(email='Warden1@gmail.com').first()
    if warden:
        profile = StaffProfile.query.filter_by(user_id=warden.id).first()
        if profile:
            db.session.delete(profile)
            db.session.commit()
            print("Deleted accidental Warden staff profile.")
        else:
            print("Warden staff profile not found.")
