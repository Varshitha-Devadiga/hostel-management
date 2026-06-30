from flask import Blueprint, render_template, abort, request, flash, redirect, url_for
from flask_login import login_required, current_user
import re
bp = Blueprint('staff', __name__, url_prefix='/staff')

@bp.before_request
@login_required
def staff_required():
    if current_user.role != 'staff':
        flash('Staff access required. Please log in as a staff member.', 'danger')
        from flask_login import logout_user
        logout_user()
        return redirect(url_for('auth.login_staff'))

@bp.route('/dashboard')
@login_required
def dashboard():
    # If the current user does not have a staff profile or role, bypass temporarily for testing purposes. 
    # Mocking the condition to prevent 403 when checking the layout.
    profile = getattr(current_user, 'staff_profile', None)
    
    from app.models.student_profile import StudentProfile
    from app.models.leave import LeaveRequest
    from datetime import date
    
    total_students = StudentProfile.query.filter_by(status='Verified').count()
    today = date.today()
    leave_count = LeaveRequest.query.filter(LeaveRequest.status == 'Approved', LeaveRequest.from_date <= today, LeaveRequest.is_returned == False).count()
    
    total_present = total_students - leave_count
    veg_count = StudentProfile.query.filter_by(status='Verified', diet='veg').count()
    nonveg_count = StudentProfile.query.filter_by(status='Verified', diet='non-veg').count()
    
    capacity = 100
    capacity_percent = int((total_students / capacity) * 100) if capacity else 0
    veg_percent = int((veg_count / total_students) * 100) if total_students else 0
    attendance_percent = int((total_present / total_students) * 100) if total_students else 0
    
    pending_leaves = LeaveRequest.query.filter_by(status='Pending').order_by(LeaveRequest.created_at.desc()).limit(3).all()
    
    from app.models.menu import FoodMenu
    import datetime
    today_menu = FoodMenu.query.filter_by(day=datetime.datetime.utcnow().strftime('%A')).first()
    today_str = datetime.datetime.utcnow().strftime('%A')
    
    # Calculate exact expected meal counts based on MealRSVP
    from app.models.meal_rsvp import MealRSVP
    expected_breakfast = total_present
    expected_lunch = total_present
    expected_snacks = total_present
    expected_dinner = total_present
    
    students_on_leave = [l.user_id for l in LeaveRequest.query.filter(LeaveRequest.status == 'Approved', LeaveRequest.from_date <= today, LeaveRequest.is_returned == False).all()]
    today_rsvps = MealRSVP.query.filter_by(date=today).all()
    
    for rsvp in today_rsvps:
        if rsvp.user_id not in students_on_leave:
            if not rsvp.eating_breakfast: expected_breakfast -= 1
            if not rsvp.eating_lunch: expected_lunch -= 1
            if not rsvp.eating_snacks: expected_snacks -= 1
            if not rsvp.eating_dinner: expected_dinner -= 1
    
    return render_template('staff/dashboard.html', 
                           profile=profile,
                           total_students=total_students,
                           total_present=total_present, 
                           veg_count=veg_count, 
                           nonveg_count=nonveg_count,
                           leave_count=leave_count,
                           capacity=capacity,
                           capacity_percent=capacity_percent,
                           veg_percent=veg_percent,
                           attendance_percent=attendance_percent,
                           pending_leaves=pending_leaves,
                           today_menu=today_menu,
                           today_str=today_str,
                           expected_breakfast=expected_breakfast,
                           expected_lunch=expected_lunch,
                           expected_snacks=expected_snacks,
                           expected_dinner=expected_dinner)

@bp.route('/shift-toggle', methods=['POST'])
@login_required
def shift_toggle():
    profile = getattr(current_user, 'staff_profile', None)
    if profile:
        from app import db
        if profile.status == 'On Duty':
            profile.status = 'On Leave'
            flash('You have successfully checked out. Have a good rest!', 'warning')
        else:
            profile.status = 'On Duty'
            flash('You have successfully checked in for your shift. Have a good day!', 'success')
        db.session.commit()
    return redirect(url_for('staff.dashboard'))

@bp.route('/students')
@login_required
def today_students():
    profile = getattr(current_user, 'staff_profile', None)
    from app.models.student_profile import StudentProfile
    from app.models.leave import LeaveRequest
    from datetime import date
    
    students = StudentProfile.query.filter_by(status='Verified').all()
    today = date.today()
    on_leave_user_ids = [l.user_id for l in LeaveRequest.query.filter(LeaveRequest.status == 'Approved', LeaveRequest.from_date <= today, LeaveRequest.is_returned == False).all()]
    
    return render_template('staff/students.html', profile=profile, students=students, on_leave_user_ids=on_leave_user_ids)

@bp.route('/food-menu')
@login_required
def food_menu():
    profile = getattr(current_user, 'staff_profile', None)
    from app.models.menu import FoodMenu
    menus = FoodMenu.query.all()
    weekly_menu = {}
    if menus:
        weekly_menu = {m.day: {'breakfast': m.breakfast, 'lunch': m.lunch, 'snacks': m.snacks, 'dinner': m.dinner} for m in menus}
    
    # Get current day
    from datetime import datetime
    today_str = datetime.now().strftime('%A')
    
    return render_template('staff/food_menu.html', profile=profile, weekly_menu=weekly_menu, today_str=today_str)

@bp.route('/food-menu/edit/<day>', methods=['POST'])
@login_required
def edit_food_menu(day):
    from app.models.menu import FoodMenu
    from app.models.notification import Notification
    from app import db
    
    menu = FoodMenu.query.filter_by(day=day).first()
    if not menu:
        menu = FoodMenu(day=day)
        db.session.add(menu)
        
    menu.breakfast = request.form.get('breakfast', '')
    menu.lunch = request.form.get('lunch', '')
    menu.snacks = request.form.get('snacks', '')
    menu.dinner = request.form.get('dinner', '')
    
    # Generate Notification
    profile = getattr(current_user, 'staff_profile', None)
    staff_name = profile.full_name if profile and profile.full_name else current_user.email.split('@')[0].capitalize()
    
    notif = Notification(
        title="Food Menu Updated",
        description=f"Staff {staff_name} has changed the food menu for {day}.",
        category="Hostel",
        priority="Normal",
        action_text="View Menu",
        action_link="/student/food-menu"
    )
    db.session.add(notif)
    db.session.commit()
    
    flash(f"The menu for {day} has been updated successfully.", "success")
    return redirect(url_for('staff.food_menu'))

@bp.route('/leaves')
@login_required
def leave_summary():
    profile = getattr(current_user, 'staff_profile', None)
    from app.models.leave import LeaveRequest
    from app.models.student_profile import StudentProfile
    from app.models.user import User
    from app import db
    
    pending_leaves = db.session.query(LeaveRequest, StudentProfile).join(User, LeaveRequest.user_id == User.id).join(StudentProfile, User.id == StudentProfile.user_id).filter(LeaveRequest.status == 'Pending').order_by(LeaveRequest.created_at.desc()).all()
    
    history_leaves = db.session.query(LeaveRequest, StudentProfile).join(User, LeaveRequest.user_id == User.id).join(StudentProfile, User.id == StudentProfile.user_id).filter(LeaveRequest.status != 'Pending').order_by(LeaveRequest.updated_at.desc()).limit(20).all()
    
    from datetime import date
    today = date.today()
    currently_away_count = LeaveRequest.query.filter(LeaveRequest.status == 'Approved', LeaveRequest.from_date <= today, LeaveRequest.is_returned == False).count()
    returns_today_count = LeaveRequest.query.filter(LeaveRequest.status == 'Approved', LeaveRequest.to_date == today).count()
    
    return render_template('staff/leaves.html', 
                           profile=profile, 
                           pending_leaves=pending_leaves, 
                           history_leaves=history_leaves,
                           currently_away_count=currently_away_count,
                           returns_today_count=returns_today_count)

@bp.route('/notifications')
@login_required
def notifications():
    profile = getattr(current_user, 'staff_profile', None)
    from app.models.notification import Notification
    notices = Notification.query.order_by(Notification.created_at.desc()).all()
    return render_template('staff/notifications.html', profile=profile, notices=notices)
@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_view():
    profile = getattr(current_user, 'staff_profile', None)
    if request.method == 'POST':
        errors = {}
        
        # Check if this is a document upload
        is_doc_upload = 'aadhaar' in request.files or 'ration_card' in request.files
        
        if not is_doc_upload:
            # Retrieve form data
            full_name = request.form.get('full_name', '').strip()
            marital_status = request.form.get('marital_status', '').strip()
            phone = request.form.get('phone', '').strip()
            # Email is read-only, so we take it from current_user
            email = current_user.email
            address = request.form.get('address', '').strip()

            # Validation rules
            if not full_name:
                errors['full_name'] = 'Full name cannot be empty.'
            if not marital_status:
                errors['marital_status'] = 'Marital status cannot be empty.'
            if not phone or not phone.isdigit() or len(phone) != 10:
                errors['phone'] = 'Mobile number must be exactly 10 digits.'
            if not address:
                errors['address'] = 'Address cannot be empty.'

            if errors:
                # Render template with errors and preserve entered data
                flash('Please correct the highlighted errors.', 'danger')
                return render_template('staff/profile.html', profile=current_user.staff_profile, errors=errors)
            else:
                # Update profile fields, create if it does not exist
                if not profile:
                    from app.models.staff_profile import StaffProfile
                    from app import db
                    profile = StaffProfile(user_id=current_user.id)  # type: ignore
                    db.session.add(profile)
                    
                profile.full_name = full_name
                profile.marital_status = marital_status
                profile.phone = phone
                profile.email = email
                profile.address = address
                
                # Handle photo upload
                photo_file = request.files.get('photo')
                if photo_file and photo_file.filename:
                    import os
                    from werkzeug.utils import secure_filename
                    from flask import current_app
                    upload_dir = os.path.join(current_app.root_path, '..', 'static', 'uploads', 'staff')
                    os.makedirs(upload_dir, exist_ok=True)
                    safe_name = secure_filename(photo_file.filename)
                    photo_file.save(os.path.join(upload_dir, safe_name))
                    profile.photo_path = safe_name
                
                from app import db
                db.session.commit()
                flash('Profile updated successfully.', 'success')
                return redirect(url_for('staff.profile_view'))
                
        else:
            # Handle Document Uploads
            if not profile:
                flash('Please save your personal information first before uploading documents.', 'warning')
                return redirect(url_for('staff.profile_view'))
                
            from app.auth.routes import verify_document_ocr
            import os
            from werkzeug.utils import secure_filename
            from flask import current_app
            
            upload_dir = os.path.join(current_app.root_path, '..', 'static', 'uploads', 'staff')
            os.makedirs(upload_dir, exist_ok=True)
            
            aadhaar_file = request.files.get('aadhaar')
            if aadhaar_file and aadhaar_file.filename:
                is_valid, msg = verify_document_ocr(aadhaar_file, "Aadhaar Card", None)
                if is_valid:
                    safe_name = secure_filename(f"aadhaar_{current_user.id}_{aadhaar_file.filename}")
                    aadhaar_file.seek(0)
                    aadhaar_file.save(os.path.join(upload_dir, safe_name))
                    profile.aadhaar_path = safe_name
                    profile.aadhaar_verified = True
                    flash('Aadhaar verified and updated.', 'success')
                else:
                    flash(msg, 'danger')

            ration_file = request.files.get('ration_card')
            if ration_file and ration_file.filename:
                is_valid, msg = verify_document_ocr(ration_file, "Ration Card", None)
                if is_valid:
                    safe_name = secure_filename(f"ration_{current_user.id}_{ration_file.filename}")
                    ration_file.seek(0)
                    ration_file.save(os.path.join(upload_dir, safe_name))
                    profile.ration_card_path = safe_name
                    profile.ration_verified = True
                    flash('Ration Card verified and updated.', 'success')
                else:
                    flash(msg, 'danger')
            
            from app import db
            db.session.commit()
            return redirect(url_for('staff.profile_view'))
    
    # Provide a fallback name from email if profile is missing
    fallback_name = current_user.email.split('@')[0].capitalize() if current_user.email else 'Staff Member'
    return render_template('staff/profile.html', profile=profile, fallback_name=fallback_name)

@bp.route('/my-leaves', methods=['GET', 'POST'])
@login_required
def my_leaves():
    profile = getattr(current_user, 'staff_profile', None)
    from app.models.leave import LeaveRequest
    from app import db
    from datetime import datetime
    
    if request.method == 'POST':
        leave_type = request.form.get('leave_type', 'casual')
        reason = request.form.get('reason')
        from_date_str = request.form.get('from_date')
        to_date_str = request.form.get('to_date')
        
        try:
            from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date() if from_date_str else datetime.utcnow().date()
            to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date() if to_date_str else datetime.utcnow().date()
        except ValueError:
            from_date = datetime.utcnow().date()
            to_date = datetime.utcnow().date()
            
        new_leave = LeaveRequest( # type: ignore
            user_id=current_user.id, # type: ignore
            leave_type=leave_type, # type: ignore
            from_date=from_date, # type: ignore
            to_date=to_date, # type: ignore
            reason=reason, # type: ignore
            status='Pending' # type: ignore
        )
        db.session.add(new_leave)
        db.session.commit()
        flash('Leave request submitted successfully.', 'success')
        return redirect(url_for('staff.my_leaves'))
        
    my_leave_history = LeaveRequest.query.filter_by(user_id=current_user.id).order_by(LeaveRequest.created_at.desc()).all()
    return render_template('staff/my_leaves.html', profile=profile, my_leave_history=my_leave_history)
