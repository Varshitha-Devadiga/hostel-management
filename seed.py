"""Seed the database with default users for each role."""
from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    db.create_all()

    # Check if users already exist to avoid duplicates
    users_to_create = [
        {"email": "admin@bcwd.in",   "role": "admin",   "password": "admin123"},
        {"email": "student@bcwd.in", "role": "student", "password": "student123"},
        {"email": "staff@bcwd.in",   "role": "staff",   "password": "staff123"},
    ]

    created = 0
    for u in users_to_create:
        existing = User.query.filter_by(email=u["email"]).first()
        if existing:
            print(f"  SKIP  {u['email']} (already exists)")
            continue
        user = User()
        user.email = u["email"]
        user.role = u["role"]
        user.set_password(u["password"])
        db.session.add(user)
        created += 1
        print(f"  ADD   {u['email']}  role={u['role']}  password={u['password']}")

    db.session.commit()
    print(f"\nDone. {created} user(s) created.")
