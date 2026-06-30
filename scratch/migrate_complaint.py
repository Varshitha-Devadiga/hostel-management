import sys
sys.path.append('e:/bcwd')
from app import create_app, db
from app.models.complaint import Complaint

app = create_app()

with app.app_context():
    db.create_all()
    print("Database tables created successfully.")
