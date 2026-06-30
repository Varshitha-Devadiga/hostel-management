import smtplib
from email.message import EmailMessage
from datetime import datetime
import os
import sys

# Add the parent directory to the path so we can import 'app'
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models.menu import FoodMenu
from app.models.user import User

# NOTE: For a real production environment, you would use a real SMTP server like SendGrid or Gmail.
# For local testing and your presentation demo, we use a local debugging server.
# To see these emails, you can run: python -m smtpd -c DebuggingServer -n localhost:1025
SMTP_SERVER = "localhost"
SMTP_PORT = 1025
SENDER_EMAIL = "warden@bcwdhostel.com"

def send_daily_menu_email():
    """Fetches today's menu and sends it to all registered students."""
    app = create_app()
    with app.app_context():
        # 1. Get today's day (e.g., "Tuesday")
        today_str = datetime.now().strftime('%A')
        
        # 2. Fetch today's menu from the database
        today_menu = FoodMenu.query.filter_by(day=today_str).first()
        
        if not today_menu:
            print(f"[{datetime.now()}] No menu found for {today_str}. Aborting email.")
            return

        # 3. Format the email content
        subject = f"BCWD Hostel Menu for Today ({today_str})"
        body = f"""
Good Morning Students,

Here is the food menu for today ({today_str}):

🥞 Breakfast: {today_menu.breakfast}
🍲 Lunch: {today_menu.lunch}
🥨 Snacks: {today_menu.snacks}
🍽️ Dinner: {today_menu.dinner}

Please ensure you mark your attendance by 10 PM. Have a great day!

- BCWD Hostel Warden
        """

        # 4. Fetch all student emails
        students = User.query.filter_by(role='student').all()
        student_emails = [student.email for student in students if student.email]

        if not student_emails:
            print(f"[{datetime.now()}] No students found to send the email to.")
            return

        # 5. Send the emails
        try:
            # We connect to the SMTP server (mock or real)
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            
            for email in student_emails:
                msg = EmailMessage()
                msg.set_content(body)
                msg['Subject'] = subject
                msg['From'] = SENDER_EMAIL
                msg['To'] = email
                
                server.send_message(msg)
                print(f"Successfully sent menu email to: {email}")
                
            server.quit()
            print(f"[{datetime.now()}] Finished sending daily menu emails.")
            
        except ConnectionRefusedError:
            print("\n[ERROR] Could not connect to the email server.")
            print("For your VIVA Demo, please explain the logic in this script.")
            print("If you want to see the emails print to the console, open a new terminal and run:")
            print("python -m smtpd -c DebuggingServer -n localhost:1025\n")
            print("--- EMAIL CONTENT THAT WOULD BE SENT ---")
            print(f"To: {len(student_emails)} students")
            print(f"Subject: {subject}")
            print(body)

if __name__ == "__main__":
    send_daily_menu_email()
