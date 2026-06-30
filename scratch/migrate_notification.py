import sys
sys.path.append('e:/bcwd')
from app import create_app, db
from app.models.notification import Notification
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    db.create_all()
    
    # Check if we already seeded
    if Notification.query.count() == 0:
        notices = [
            Notification(
                title="SSP Scholarship 2023-24 Deadline Extension",
                description="The deadline for post-matric scholarship applications has been extended to November 15th. All students who haven't submitted their Aadhar-seeded bank details are advised to do so immediately at the hostel office.",
                category="Scholarship",
                action_text="Apply Now",
                action_link="#",
                created_at=datetime.utcnow() - timedelta(days=1)
            ),
            Notification(
                title="Hostel Committee Monthly Meet",
                description="Monthly student grievance meeting will be held in the main hall. Agenda includes mess menu revisions and hostel security scheduling. Attendance is mandatory for all floor representatives.",
                category="Meeting",
                created_at=datetime.utcnow() - timedelta(days=2)
            ),
            Notification(
                title="Ayudha Puja Break",
                description="The hostel mess will be closed for two meals on Oct 23rd for Ayudha Puja. Students planning to stay back are requested to register their names at the security desk by Saturday evening.",
                category="Holiday",
                action_text="Register Stay",
                action_link="#",
                created_at=datetime.utcnow() - timedelta(days=5)
            ),
            Notification(
                title="New Mess Timings",
                description="Starting next Monday, breakfast will be served from 7:15 AM to cater to the first shift students. Evening tea is shifted to 5:00 PM.",
                category="Hostel",
                action_text="View Menu",
                action_link="/student/food-menu",
                image_url="https://images.unsplash.com/photo-1541844053589-346841d0b34c?w=400&q=80",
                created_at=datetime.utcnow() - timedelta(days=7)
            ),
            Notification(
                title="Maintenance - Boiler Water Heater",
                description="Routine maintenance of solar heaters on Block B is scheduled for Wednesday. Hot water supply may be interrupted between 10:00 AM and 4:00 PM.",
                category="Hostel",
                priority="High",
                created_at=datetime.utcnow() - timedelta(days=10)
            ),
            Notification(
                title="Fee Reimbursement Portal Open",
                description="Students from category I, IIA, IIB, and IIIB can now apply for fee reimbursement on the official portal. Required documents: Income certificate and college admission fee receipt.",
                category="Scholarship",
                action_text="Apply Now",
                action_link="#",
                created_at=datetime.utcnow() - timedelta(days=15)
            )
        ]
        
        db.session.add_all(notices)
        db.session.commit()
        print("Database tables created and seeded successfully.")
    else:
        print("Database tables created successfully (already seeded).")
