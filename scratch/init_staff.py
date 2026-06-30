from app import create_app
from app.models import db, User
from app.models.staff_profile import StaffProfile

app = create_app()
with app.app_context():
    db.create_all()
    # add dummy staff
    dummies = [
        ("Anita Hegde", "anita@example.com", "Senior Warden", "+91 98765 43210", "On Duty"),
        ("Rajesh Kumar", "rajesh@example.com", "Security Head", "+91 99887 66554", "On Duty"),
        ("Sunitha Rao", "sunitha@example.com", "Hostel Admin", "+91 97766 55443", "On Leave"),
        ("Manjunath P.", "manjunath@example.com", "Maintenance Supervisor", "+91 94433 22110", "On Duty"),
    ]
    for name, email, role, phone, status in dummies:
        if not User.query.filter_by(email=email).first():
            u = User(email=email, role='staff')
            u.set_password('1234')
            db.session.add(u)
            db.session.flush()
            sp = StaffProfile(user_id=u.id, full_name=name, specialty=role, phone=phone, status=status)
            db.session.add(sp)
    db.session.commit()
    print("Database synced successfully with dummy data.")
