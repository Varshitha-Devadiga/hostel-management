from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from werkzeug.utils import secure_filename
import os
from flask_login import login_required, current_user, login_user, logout_user
import pytesseract
from PIL import Image
from ..auth.forms import LoginForm, StudentRegistrationForm
from app import db
from app.models.student_profile import StudentProfile
from . import auth_bp


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return redirect(url_for('auth.login_student'))

@auth_bp.route('/login/student', methods=['GET', 'POST'])
def login_student():
    form = LoginForm()
    if form.validate_on_submit():
        from app.models.user import User
        user = User.query.filter(User.email.ilike(form.email.data)).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            
            if user.role == 'student':
                flash('Successfully logged in as Student!', 'success')
                return redirect(url_for('student.dashboard'))
            elif user.role == 'staff':
                flash('Successfully logged in as Staff!', 'success')
                return redirect(url_for('staff.dashboard'))
            elif user.role == 'admin':
                flash('Successfully logged in as Admin!', 'success')
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('student/login.html', form=form)

@auth_bp.route('/login/warden', methods=['GET', 'POST'])
def warden_login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password')
        
        # Here we hardcode the warden check since they are an admin
        # Or you could query a specific admin user from db if they exist
        from app.models.user import User
        # Use ilike for case-insensitive email matching
        user = User.query.filter(User.email.ilike(email), User.role == 'admin').first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Successfully logged in as Warden!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
            
    return render_template('admin/login.html')

@auth_bp.route('/login/staff', methods=['GET', 'POST'])
def login_staff():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password')
        
        from app.models.user import User
        user = User.query.filter(User.email.ilike(email), User.role == 'staff').first()
        
        if not user:
            flash('This email is not registered. Please register first.', 'danger')
            return redirect(url_for('auth.login_staff'))
            
        if user.check_password(password):
            login_user(user)
            
            # Ensure staff profile exists upon first login
            if not getattr(user, 'staff_profile', None):
                from app.models.staff_profile import StaffProfile
                fallback_name = user.email.split('@')[0].capitalize() if user.email else 'Staff Member'
                sp = StaffProfile(user_id=user.id, full_name=fallback_name, specialty='General Staff')
                db.session.add(sp)
                db.session.commit()
                
            flash('Successfully logged in as Staff!', 'success')
            return redirect(url_for('staff.dashboard'))
        else:
            flash('Invalid password. Please try again.', 'danger')
            return redirect(url_for('auth.login_staff'))
            
    return render_template('auth/login_staff.html')

@auth_bp.route('/register/staff', methods=['GET', 'POST'])
def register_staff():
    if request.method == 'POST':
        # Mock staff registration logic
        return redirect(url_for('auth.login_staff'))
    return render_template('auth/register_staff.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login_student'))


def verify_document_ocr(file_obj, document_type, expected_number):
    """
    Strictly verifies that the uploaded document image contains the exact expected number.
    """
    if not file_obj or not getattr(file_obj, 'filename', None):
        return False, "No file uploaded. Please upload a valid document."
        
    try:
        # Save current file position
        file_obj.seek(0)
        img = Image.open(file_obj)
        
        # Windows Path for Tesseract
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
        extracted_text = pytesseract.image_to_string(img)
        
        # Reset file position after reading
        file_obj.seek(0)
        
        # Normalize extracted text by removing whitespace and special characters
        import re
        normalized_text = re.sub(r'\s+', '', extracted_text)
        normalized_expected = re.sub(r'\s+', '', str(expected_number)) if expected_number else ""
        
        if normalized_expected:
            if normalized_expected in normalized_text:
                return True, f"{document_type} verified successfully."
            else:
                return False, f"Could not verify {document_type}. The entered number was not found in the uploaded image. Please ensure the image is clear and matches the number provided."
        else:
            # If no expected number is provided, we verify it by checking for expected patterns in the document
            if "Aadhaar" in document_type:
                if re.search(r'\d{12}', normalized_text):
                    return True, f"{document_type} verified successfully."
                else:
                    return False, f"Could not verify {document_type}. No valid 12-digit Aadhaar number found in the uploaded image."
            elif "Ration" in document_type:
                if re.search(r'\d{10,15}', normalized_text) or re.search(r'[A-Z0-9]{10,15}', normalized_text):
                    return True, f"{document_type} verified successfully."
                else:
                    return False, f"Could not verify {document_type}. No valid Ration Card number found in the uploaded image."
            
            # Fallback for unknown document types
            return True, f"{document_type} accepted."
            
    except pytesseract.TesseractNotFoundError:
        # Strict mode: fail if Tesseract is missing
        file_obj.seek(0)
        current_app.logger.warning("Tesseract OCR not found. Failing validation.")
        return False, "OCR engine not available. Please contact administrator."
    except Exception as e:
        file_obj.seek(0)
        current_app.logger.error(f"OCR Verification error: {str(e)}")
        return False, f"OCR processing failed. Please ensure the image is clear."

@auth_bp.route('/register/student/wizard', methods=['GET', 'POST'])
def register_student_wizard():
    form = StudentRegistrationForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            # Run OCR validation before DB creation
            aadhaar_file = form.aadhaar.data
            clean_aadhaar_num = form.aadhaar_number.data.replace(' ', '')
            is_valid_aadhaar, aadhaar_msg = verify_document_ocr(aadhaar_file, "Aadhaar Card", clean_aadhaar_num)
            if not is_valid_aadhaar:
                flash(aadhaar_msg, 'danger')
                return render_template('student/register_wizard.html', form=form)
                
            ration_file = form.ration_card.data
            is_valid_ration, ration_msg = verify_document_ocr(ration_file, "Ration Card", form.ration_card_number.data)
            if not is_valid_ration:
                flash(ration_msg, 'danger')
                return render_template('student/register_wizard.html', form=form)
                
            try:
                # 1. Create the associated User first
                from app.models.user import User
                new_user = User(email=form.email.data, role='student')
                new_user.set_password(form.password.data)
                db.session.add(new_user)
                db.session.flush()  # obtain new_user.id without committing

                # 2. Establish safe target path directory for uploads
                upload_dir = os.path.join(current_app.root_path, '..', 'static', 'uploads')
                os.makedirs(upload_dir, exist_ok=True)

                def save_file(field_name):
                    file_obj = getattr(form, field_name).data
                    if file_obj and hasattr(file_obj, 'filename') and file_obj.filename:
                        safe_name = secure_filename(file_obj.filename)
                        file_obj.save(os.path.join(upload_dir, safe_name))
                        return safe_name
                    return None

                photo_fname = save_file('photo')
                aadhaar_fname = save_file('aadhaar')
                ration_fname = save_file('ration_card')
                college_id_fname = save_file('college_id')

                # 3. Create the StudentProfile linked to the new user
                new_student = StudentProfile(
                    user_id=new_user.id,
                    full_name=form.full_name.data,
                    dob=form.dob.data,
                    mobile=form.mobile.data,
                    father_name=form.father_name.data,
                    mother_name=form.mother_name.data,
                    guardian_mobile=form.guardian_mobile.data,
                    emergency_contact=form.emergency_contact.data,
                    college=form.college.data,
                    university=form.university.data,
                    course=form.course.data,
                    semester=form.semester.data,
                    admission_year=form.admission_year.data,
                    course_duration=int(form.course_duration.data),
                    completion_year=form.completion_year.data,
                    hod_name=form.hod_name.data,
                    hod_phone=form.hod_phone.data,
                    diet=form.diet.data,
                    food_items=form.food_items.data or [],
                    aadhaar_number=clean_aadhaar_num,
                    ration_card_number=form.ration_card_number.data,
                    aadhaar_path=aadhaar_fname,
                    ration_card_path=ration_fname,
                    college_id_path=college_id_fname,
                    agreed=form.agree.data,
                )
                db.session.add(new_student)
                db.session.commit()

                # Send Welcome Email with Time-Sensitive Menu
                try:
                    from app.utils.email import send_notification_email
                    from app.models.menu import FoodMenu
                    from datetime import datetime
                    
                    now = datetime.now()
                    today_menu = FoodMenu.query.filter_by(day=now.strftime('%A')).first()
                    if today_menu:
                        hour = now.hour
                        menu_text = f"Welcome to BCWD Hostel, {form.full_name.data}!\n\nHere is the food menu for the rest of today ({now.strftime('%A')}):\n\n"
                        
                        if hour < 10:
                            menu_text += f"- Breakfast: {today_menu.breakfast}\n"
                        if hour < 14:
                            menu_text += f"- Lunch: {today_menu.lunch}\n"
                        if hour < 18:
                            menu_text += f"- Snacks: {today_menu.snacks}\n"
                        if hour < 22:
                            menu_text += f"- Dinner: {today_menu.dinner}\n"
                            
                        menu_text += "\nYou can log in to your student dashboard anytime to set your daily meal preferences. Note that past meals for today are automatically disabled.\n\nRegards,\nBCWD Administration"
                        
                        send_notification_email("Welcome to BCWD Hostel - Today's Menu", menu_text, [form.email.data])
                except Exception as e:
                    current_app.logger.error(f"Failed to send welcome email: {e}")

                flash("Registration successful! A welcome email with today's menu has been sent to your inbox. Please login.", 'success')
                return redirect(url_for('auth.login_student'))

            except Exception as e:
                db.session.rollback()
                current_app.logger.error(f"Registration error: {e}")
                error_msg = str(e)
                if 'UNIQUE constraint failed' in error_msg and 'email' in error_msg:
                    flash('This email is already registered. Please use a different email or login.', 'danger')
                else:
                    flash(f'Registration failed. Please try again.', 'danger')
        else:
            # Form didn't validate — show errors
            current_app.logger.warning(f"Form validation errors: {form.errors}")
            error_details = []
            for field_name, errors in form.errors.items():
                field_label = getattr(form, field_name).label.text
                error_details.append(f"• <b>{field_label}:</b> {errors[0]}")
            
            if error_details:
                error_msg = 'Please fix the following errors:<br><div style="text-align: left; margin-top: 10px;">' + '<br>'.join(error_details) + '</div>'
                flash(error_msg, 'danger')
            else:
                flash('Please fix the errors below and resubmit.', 'danger')

    return render_template('student/register_wizard.html', form=form)