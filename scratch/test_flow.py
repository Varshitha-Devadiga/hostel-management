import io
from app import create_app, db
from app.models import User, Student, StudentProfile

app = create_app()
app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for programmatic test

def test_full_workflow():
    client = app.test_client()

    print("Cleaning database...")
    with app.app_context():
        # Remove any existing user
        User.query.filter_by(email="flow_test@123.com").delete()
        db.session.commit()

    # 1. Test Registration Wizard GET
    print("GETing registration wizard...")
    resp = client.get('/register/student/wizard')
    if resp.status_code != 200:
        print(f"FAILED: GET /register/student/wizard returned {resp.status_code}")
        return False
    print("Registration wizard page loads successfully.")

    # 2. Test Registration Wizard POST
    aadhaar_file = (io.BytesIO(b"aadhaar data"), "aadhaar.pdf")
    ration_file = (io.BytesIO(b"ration data"), "ration.pdf")
    college_id_file = (io.BytesIO(b"college id data"), "college_id.pdf")

    post_data = {
        "email": "flow_test@123.com",
        "password": "mysecretpassword",
        "confirm_password": "mysecretpassword",
        "full_name": "Flow Test Student",
        "dob": "2002-05-15",
        "mobile": "9876543210",
        "father_name": "Father Flow",
        "mother_name": "Mother Flow",
        "guardian_name": "Guardian Flow",
        "guardian_mobile": "9876543211",
        "college": "Flow College",
        "university": "Flow Uni",
        "course": "Computer Science",
        "semester": "1",
        "admission_year": "2024",
        "course_duration": "4",
        "hod_name": "Dr. Flow",
        "hod_phone": "9876543212",
        "diet": "veg",
        "food_items": ["egg"],
        "aadhaar": aadhaar_file,
        "ration_card": ration_file,
        "college_id": college_id_file,
        "agree": "y"
    }

    print("Submitting registration form...")
    resp = client.post('/register/student/wizard', data=post_data, content_type='multipart/form-data')
    # Successful registration should redirect (302) to auth.login_student
    print(f"Registration POST status code: {resp.status_code}, redirect location: {resp.headers.get('Location')}")
    if resp.status_code != 302:
        print("FAILED: Registration did not redirect.")
        # print form error indicators if any
        print(resp.data.decode('utf-8')[:2000])
        return False

    # 3. Test Database Integrity
    with app.app_context():
        user = User.query.filter_by(email="flow_test@123.com").first()
        if not user:
            print("FAILED: User was not created in database.")
            return False
        student = Student.query.filter_by(user_id=user.id).first()
        if not student or student.name != "Flow Test Student":
            print("FAILED: Student record was not created/linked correctly.")
            return False
        profile = StudentProfile.query.filter_by(user_id=user.id).first()
        if not profile or profile.mobile != "9876543210":
            print("FAILED: StudentProfile record was not created correctly.")
            return False
        print("Database record verification: SUCCESS!")

    # 4. Test Student Login POST
    print("Logging in with registered credentials...")
    login_data = {
        "email": "flow_test@123.com",
        "password": "mysecretpassword",
        "remember": "y"
    }
    resp = client.post('/login/student', data=login_data)
    print(f"Login POST status code: {resp.status_code}, redirect location: {resp.headers.get('Location')}")
    if resp.status_code != 302 or '/dashboard' not in resp.headers.get('Location', ''):
        print("FAILED: Login did not redirect to dashboard.")
        print(resp.data.decode('utf-8')[:1000])
        return False

    print("--- ALL TESTS PASSED SUCCESSFULLY! WORKFLOW IS FULLY FUNCTIONAL ---")
    return True

if __name__ == "__main__":
    test_full_workflow()
