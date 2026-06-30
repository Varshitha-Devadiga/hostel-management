import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from threading import Thread
from flask import current_app

def send_async_email(app, msg, recipients):
    """
    Sends the email asynchronously in a background thread.
    Uses simulated mode if credentials are not provided.
    """
    with app.app_context():
        mail_user = os.environ.get('MAIL_USERNAME')
        mail_pass = os.environ.get('MAIL_PASSWORD')

        if not mail_user or not mail_pass:
            # SIMULATION MODE
            app.logger.info("\n" + "="*50)
            app.logger.info("📧 SIMULATED EMAIL NOTIFICATION")
            app.logger.info(f"To: {', '.join(recipients)}")
            app.logger.info(f"Subject: {msg['Subject']}")
            app.logger.info("-"*50)
            app.logger.info(msg.get_payload())
            app.logger.info("="*50 + "\n")
            return

        # REAL EMAIL MODE
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(mail_user, mail_pass)
            server.sendmail(mail_user, recipients, msg.as_string())
            server.quit()
            app.logger.info(f"Real email successfully sent to {len(recipients)} recipients.")
        except Exception as e:
            app.logger.error(f"Failed to send email: {e}")

def send_notification_email(subject, body, recipients):
    """
    Prepares the email and spawns a background thread to send it.
    """
    if not recipients:
        return
        
    sender = os.environ.get('MAIL_USERNAME', 'hostel_admin@bcwd.com')
    
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = "undisclosed-recipients:;"
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    app = current_app._get_current_object()
    thread = Thread(target=send_async_email, args=(app, msg, recipients))
    thread.start()
