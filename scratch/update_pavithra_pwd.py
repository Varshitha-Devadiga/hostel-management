import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import db
from app.models.user import User

app = create_app()

with app.app_context():
    user = User.query.filter_by(email='pavithra@gmail.com').first()
    if user:
        user.set_password('123456')
        db.session.commit()
        print("Updated pavithra@gmail.com password to 123456")
    else:
        print("User not found!")
