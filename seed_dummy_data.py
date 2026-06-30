import sys
import os
from datetime import datetime, date, timedelta
from werkzeug.security import generate_password_hash

# Add the parent directory to the path so we can import 'app'
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db, bcrypt
from app.models.user import User
from app.models.student_profile import StudentProfile
from app.models.staff_profile import StaffProfile
from app.models.menu import FoodMenu
from app.models.leave import LeaveRequest

def seed_data():
    app = create_app()
    with app.app_context():
        print("Seeding dummy data for your presentation...")
        
        # 1. Ensure a Warden (Admin) exists
        warden = User.query.filter_by(role='admin').first()
        if not warden:
            print("Creating Warden account: warden@bcwd.com / password123")
            warden = User(email='warden@bcwd.com', role='admin')
            warden.set_password('password123')
            db.session.add(warden)
        
        # 2. Ensure a Staff member exists
        staff = User.query.filter_by(role='staff').first()
        if not staff:
            print("Creating Staff account: staff@bcwd.com / password123")
            staff = User(email='staff@bcwd.com', role='staff')
            staff.set_password('password123')
            db.session.add(staff)
            db.session.flush()
            staff_prof = StaffProfile(user_id=staff.id, full_name='Demo Staff', phone='9876543210', gender='Female', address='Mangalore', specialty='Kitchen', status='On Duty')
            db.session.add(staff_prof)
            
        # 3. Ensure a Student exists
        student = User.query.filter_by(role='student').first()
        if not student:
            print("Creating Student account: student@bcwd.com / password123")
            student = User(email='student@bcwd.com', role='student')
            student.set_password('password123')
            db.session.add(student)
            db.session.flush()
            student_prof = StudentProfile(
                user_id=student.id, full_name='Demo Student', phone='1234567890', 
                gender='Female', dob=date(2005, 1, 1), 
                address='Bangalore', institution='Govt College', 
                course='B.Sc', semester='3', admission_year='2025', diet='veg'
            )
            db.session.add(student_prof)

        # 4. Populate Food Menu for all days (so next meal always works)
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for day in days:
            menu = FoodMenu.query.filter_by(day=day).first()
            if not menu:
                menu = FoodMenu(day=day)
                db.session.add(menu)
            
            # Update the menus with good looking dummy food
            menu.breakfast = "Idli, Vada, Sambar, Coconut Chutney"
            menu.lunch = "Rice, Dal, Mixed Veg Curry, Curd"
            menu.snacks = "Tea, Biscuits, Bajji"
            menu.dinner = "Chapati, Paneer Butter Masala, Rice"
            
            # Maybe make Wednesday and Sunday non-veg friendly for variety
            if day in ['Wednesday', 'Sunday']:
                menu.lunch = "Chicken Biryani / Veg Biryani, Raita"
                menu.dinner = "Chicken Curry / Gobi Manchurian, Rice, Roti"

        # 5. Create some pending Leave Requests for the admin dashboard
        today = date.today()
        if student:
            # Check if pending leaves exist
            pending = LeaveRequest.query.filter_by(user_id=student.id, status='Pending').first()
            if not pending:
                print("Creating a pending leave request...")
                leave = LeaveRequest(
                    user_id=student.id,
                    leave_type='weekend',
                    from_date=today + timedelta(days=2),
                    to_date=today + timedelta(days=4),
                    reason='Going home for weekend',
                    status='Pending'
                )
                db.session.add(leave)

        db.session.commit()
        print("\nAll dummy data seeded successfully! Your 3 modules are ready to present.")
        print("---")
        print("Use these test accounts if needed:")
        print("Student: student@bcwd.com | Pass: password123")
        print("Staff:   staff@bcwd.com   | Pass: password123")
        print("Admin:   warden@bcwd.com  | Pass: password123")

if __name__ == '__main__':
    seed_data()
