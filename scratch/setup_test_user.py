import datetime
from app import create_app, db
from app.models import User, Student, StudentProfile

app = create_app()
with app.app_context():
    # Remove existing test user
    User.query.filter_by(email="student@123.com").delete()
    User.query.filter_by(email="student@123").delete()
    db.session.commit()

    # Create student@123.com
    u = User(email="student@123.com", role="student")
    u.set_password("123456")
    db.session.add(u)
    db.session.flush()

    s = Student(user_id=u.id, name="Test Student", dob=datetime.date(2000, 1, 1))
    db.session.add(s)

    p = StudentProfile(
        user_id=u.id,
        full_name="Test Student",
        dob=datetime.date(2000, 1, 1),
        mobile="9876543210",
        father_name="Father Name",
        mother_name="Mother Name",
        guardian_name="Guardian Name",
        guardian_mobile="9876543211",
        college="College of Engineering",
        university="State University",
        course="B.E.",
        semester="1st Semester",
        admission_year=2024,
        course_duration=4,
        hod_name="Dr. Smith",
        hod_phone="9876543212",
        diet="veg",
        food_items=["egg"],
        agreed=True
    )
    db.session.add(p)
    db.session.commit()
    # Create admin user
    User.query.filter_by(email="Warden1@gmail.com").delete()
    db.session.commit()

    admin_u = User(email="Warden1@gmail.com", role="admin")
    admin_u.set_password("padil@123")
    db.session.add(admin_u)
    db.session.commit()
    print("User Warden1@gmail.com / padil@123 created successfully!")
