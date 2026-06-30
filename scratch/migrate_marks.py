import sys
sys.path.append('e:/bcwd')
from app import create_app, db
from app.models.marks_card import MarksCard, MarksTimeline

app = create_app()

with app.app_context():
    db.create_all()
    print("Database tables created successfully.")
