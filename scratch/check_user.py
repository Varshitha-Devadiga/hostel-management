import os
from app import create_app, db
from app.models.user import User

app = create_app()
with app.app_context():
    user = User.query.filter_by(email='test_student2@example.com').first()
    if user:
        print('User found: ID', user.id, 'role', user.role)
    else:
        print('User not found')
