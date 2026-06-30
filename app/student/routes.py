from flask import render_template, abort, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.student_profile import StudentProfile
from app.models.leave import LeaveRequest
from app.models.menu import FoodMenu
from app.models.meal_rsvp import MealRSVP
from app.models.marks_card import MarksCard, MarksTimeline
from datetime import datetime
import os
import re
from PIL import Image
import pytesseract
from werkzeug.utils import secure_filename
from flask import current_app, send_from_directory
from . import student_bp

def verify_marks_card_ocr(file_obj, semester):
    if not file_obj or not getattr(file_obj, 'filename', None):
        return False, "No file uploaded", None
        
    try:
        file_obj.seek(0)
        img = Image.open(file_obj)
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        extracted_text = pytesseract.image_to_string(img)
        file_obj.seek(0)
        
        text_upper = extracted_text.upper()
        
        # Look for CGPA or SGPA
        cgpa_match = re.search(r'(?:CGPA|SGPA)[\s:]*([\d.]+)', text_upper)
        extracted_cgpa = cgpa_match.group(1) if cgpa_match else None
        
        if "UNIVERSITY" in text_upper or "MARKS" in text_upper or extracted_cgpa:
            return True, "Marks Card automatically verified by OCR.", extracted_cgpa
        else:
            return False, "OCR could not detect marks card details. Please ensure the image is clear.", None
            
    except pytesseract.TesseractNotFoundError:
        file_obj.seek(0)
        return False, "OCR engine not available. Marked as Pending.", None
    except Exception as e:
        file_obj.seek(0)
        return False, f"OCR processing failed: {str(e)}", None

def process_fest_letter_ocr(file_obj):
    if not file_obj or not getattr(file_obj, 'filename', None):
        return False, "No file uploaded", None, None
        
    try:
        file_obj.seek(0)
        img = Image.open(file_obj)
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        extracted_text = pytesseract.image_to_string(img)
        file_obj.seek(0)
        
        text_lower = extracted_text.lower()
        
        # Simple date regex DD/MM/YYYY or MM-DD-YYYY or DD-MM-YYYY
        date_pattern = r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'
        dates_found = re.findall(date_pattern, text_lower)
        extracted_dates = ", ".join(dates_found) if dates_found else None
        
        # Simple days regex (e.g. "2 days", "two days")
        days_pattern = r'\b(\d+|one|two|three|four|five|six|seven|eight|nine|ten)\s+days?\b'
        days_match = re.search(days_pattern, text_lower)
        extracted_days = None
        if days_match:
            val = days_match.group(1)
            if val.isdigit():
                extracted_days = int(val)
            else:
                word_to_num = {'one':1, 'two':2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8, 'nine':9, 'ten':10}
                extracted_days = word_to_num.get(val, None)
                
        # Basic validation: If it mentions "fest", "cultural", "event", "sports" or we found dates
        is_valid = any(kw in text_lower for kw in ["fest", "cultural", "event", "sports", "permission", "leave"]) or bool(extracted_dates)
        
        return is_valid, extracted_text, extracted_dates, extracted_days
            
    except pytesseract.TesseractNotFoundError:
        file_obj.seek(0)
        return False, "OCR engine not available.", None, None
    except Exception as e:
        file_obj.seek(0)
        return False, f"OCR processing failed: {str(e)}", None, None

@student_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if current_user.role != 'student':
        if current_user.role == 'staff':
            return redirect(url_for('staff.dashboard'))
        elif current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        else:
            abort(403)
        
    # 1. Fetch User Profile
    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    
    # 2. Fetch Active Leave Status (Count pending requests)
    pending_leaves = LeaveRequest.query.filter_by(user_id=current_user.id, status='Pending').count()
    
    # 3. Fetch Today's Menu and calculate Next Meal
    now = datetime.now()
    today_menu = FoodMenu.query.filter_by(day=now.strftime('%A')).first()
    
    hour = now.hour
    if hour < 10:
        next_meal_name = "Breakfast"
        next_meal_food = today_menu.breakfast if today_menu else None
    elif hour < 14:
        next_meal_name = "Lunch"
        next_meal_food = today_menu.lunch if today_menu else None
    elif hour < 18:
        next_meal_name = "Snacks"
        next_meal_food = today_menu.snacks if today_menu else None
    elif hour < 22:
        next_meal_name = "Dinner"
        next_meal_food = today_menu.dinner if today_menu else None
    else:
        from datetime import timedelta
        tomorrow_menu = FoodMenu.query.filter_by(day=(now + timedelta(days=1)).strftime('%A')).first()
        next_meal_name = "Breakfast"
        next_meal_food = tomorrow_menu.breakfast if tomorrow_menu else None
        
    # 4. Check for missing marks cards
    missing_marks_cards = 0
    if profile and profile.semester and profile.semester.isdigit():
        current_sem = int(profile.semester)
        if current_sem > 1:
            uploaded_count = MarksCard.query.filter_by(user_id=current_user.id).count()
            expected_count = current_sem - 1
            if uploaded_count < expected_count:
                missing_marks_cards = expected_count - uploaded_count
    # 5. Handle Meal RSVP
    from datetime import date
    today_date = date.today()
    rsvp = MealRSVP.query.filter_by(user_id=current_user.id, date=today_date).first()
    
    if request.method == 'POST' and 'rsvp_submit' in request.form:
        if not rsvp:
            rsvp = MealRSVP(user_id=current_user.id, date=today_date)
            # Default everything to True if creating fresh, then override with form data if time allows
            rsvp.eating_breakfast = True
            rsvp.eating_lunch = True
            rsvp.eating_snacks = True
            rsvp.eating_dinner = True
            db.session.add(rsvp)
            
        if hour < 6:
            rsvp.eating_breakfast = 'breakfast' in request.form
        if hour < 10:
            rsvp.eating_lunch = 'lunch' in request.form
        if hour < 15:
            rsvp.eating_snacks = 'snacks' in request.form
        if hour < 17:
            rsvp.eating_dinner = 'dinner' in request.form
        
        db.session.commit()
        flash("Your meal RSVP has been updated!", "success")
        return redirect(url_for('student.dashboard'))
        
    # If no RSVP exists yet, create a default one for display purposes (but don't save to db until they submit, or we can assume True)
    if not rsvp:
        class DefaultRSVP:
            eating_breakfast = True
            eating_lunch = True
            eating_snacks = True
            eating_dinner = True
        rsvp = DefaultRSVP()

    return render_template('student/dashboard.html', 
                           profile=profile, 
                           pending_leaves=pending_leaves,
                           next_meal_name=next_meal_name,
                           next_meal_food=next_meal_food,
                           missing_marks_cards=missing_marks_cards,
                           rsvp=rsvp,
                           current_hour=hour)


@student_bp.route('/leave-outpass', methods=['GET', 'POST'])
@login_required
def leave_outpass():
    if current_user.role != 'student':
        abort(403)
        
    active_leave = LeaveRequest.query.filter(
        LeaveRequest.user_id == current_user.id,
        LeaveRequest.status.in_(['Pending', 'Approved']),
        LeaveRequest.is_returned == False
    ).first()
    has_active_leave = bool(active_leave)

    if request.method == 'POST':
        if has_active_leave:
            flash('You already have an active or pending leave request. You can extend your approved leave if needed.', 'danger')
            return redirect(url_for('student.leave_outpass'))

        from_date_str = request.form.get('from_date')
        to_date_str = request.form.get('to_date')
        reason = request.form.get('reason')
        leave_type = request.form.get('leave_type', 'holiday')
        
        shift_type = request.form.get('shift_type') if leave_type == 'nursing_duty' else None
        expected_return_time = request.form.get('expected_return_time') if leave_type == 'nursing_duty' else None
        
        try:
            from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date() if from_date_str else datetime.utcnow().date()
            to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date() if to_date_str else datetime.utcnow().date()
        except ValueError:
            from_date = datetime.utcnow().date()
            to_date = datetime.utcnow().date()
            
        new_request = LeaveRequest(
            user_id=current_user.id,
            leave_type=leave_type,
            from_date=from_date,
            to_date=to_date,
            reason=reason,
            shift_type=shift_type,
            expected_return_time=expected_return_time
        )
        
        # Handle College Fest Attachment & OCR
        if leave_type == 'college_fest':
            file = request.files.get('attachment')
            if file and file.filename != '':
                filename = secure_filename(f"fest_{current_user.id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{file.filename}")
                upload_path = os.path.join(current_app.root_path, 'static', 'uploads', 'leaves')
                os.makedirs(upload_path, exist_ok=True)
                file_path_full = os.path.join(upload_path, filename)
                file.save(file_path_full)
                new_request.attachment_path = filename
                
                # Auto-verify with OCR
                with open(file_path_full, 'rb') as f:
                    is_valid, ocr_text, ocr_dates, ocr_days = process_fest_letter_ocr(f)
                    
                new_request.ocr_text = ocr_text
                new_request.ocr_extracted_dates = ocr_dates
                new_request.ocr_days = ocr_days
                
                if is_valid:
                    new_request.status = 'Approved'
                    from app.models.notification import Notification
                    student_name = current_user.student_profile.full_name if current_user.student_profile else "Student"
                    notif = Notification(
                        title="College Fest Leave Auto-Approved",
                        description=f"{student_name}'s College Fest late pass was scanned and auto-approved.",
                        category="Hostel",
                        priority="Normal",
                        target_user_id=None,
                        target_role="warden"
                    )
                    db.session.add(notif)
                    flash('Your College Fest leave has been auto-approved based on the uploaded letter!', 'success')
                else:
                    flash('Your College Fest leave has been submitted and is pending manual review.', 'info')

        db.session.add(new_request)
        db.session.commit()
        if leave_type != 'college_fest' or new_request.status != 'Approved':
            flash('Your leave request has been submitted successfully.', 'success')
        return redirect(url_for('student.leave_outpass'))

    history = LeaveRequest.query.filter_by(user_id=current_user.id).order_by(LeaveRequest.created_at.desc()).all()
    return render_template('student/leave_outpass.html', history=history, has_active_leave=has_active_leave)

@student_bp.route('/return-confirmation/<int:leave_id>', methods=['GET', 'POST'])
@login_required
def return_confirmation(leave_id):
    if current_user.role != 'student':
        abort(403)
        
    leave = LeaveRequest.query.filter_by(id=leave_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        return_time = request.form.get('return_time')
        return_notes = request.form.get('return_notes')
        
        leave.is_returned = True
        leave.return_time = return_time
        leave.return_notes = return_notes
        db.session.commit()
        
        return redirect(url_for('student.leave_outpass'))
        
    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    today_menu = FoodMenu.query.filter_by(day=datetime.utcnow().strftime('%A')).first()
    return render_template('student/return_confirmation.html', leave=leave, profile=profile, menu=today_menu)


@student_bp.route('/leave/extend/<int:leave_id>', methods=['POST'])
@login_required
def extend_leave(leave_id):
    if current_user.role != 'student':
        abort(403)
        
    leave = LeaveRequest.query.filter_by(id=leave_id, user_id=current_user.id).first_or_404()
    
    if leave.status == 'Approved' and not leave.is_returned:
        new_date_str = request.form.get('new_date')
        extension_reason = request.form.get('reason')
        
        try:
            new_date = datetime.strptime(new_date_str, '%Y-%m-%d').date()
            
            old_date = leave.to_date
            leave.to_date = new_date
            leave.reason = leave.reason + f"\n\n[Extended from {old_date} to {new_date}. Reason: {extension_reason}]"
            
            db.session.commit()
            
            # Send Notification to Warden
            from app.utils.email import send_notification_email
            student_profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
            student_name = student_profile.full_name if student_profile else f"Student ID #{current_user.id}"
            
            warden_email = "warden@bcwd.gov.in"
            subject = f"Leave Extension: {student_name}"
            body = f"Hello Warden,\n\n{student_name} has extended their leave return date from {old_date} to {new_date}.\n\nReason: {extension_reason}\n\nThis extension was auto-recorded in the system.\n\nRegards,\nBCWD Notification System"
            send_notification_email(subject, body, [warden_email])
            
            flash('Your leave has been successfully extended.', 'success')
            
        except ValueError:
            flash('Invalid date format.', 'danger')
    else:
        flash('Cannot extend this leave request.', 'danger')
        
    return redirect(url_for('student.leave_outpass'))


@student_bp.route('/food-menu')
@login_required
def food_menu():
    if current_user.role != 'student':
        abort(403)
        
    from app.models.menu import FoodMenu
    menus = FoodMenu.query.all()
    weekly_menu = {}
    
    if not menus:
        # Fallback if DB is empty, though admin route seeds it
        weekly_menu = {
            'Monday': {'breakfast': 'Coming Soon', 'lunch': 'Coming Soon', 'snacks': 'Coming Soon', 'dinner': 'Coming Soon'},
            'Tuesday': {'breakfast': 'Coming Soon', 'lunch': 'Coming Soon', 'snacks': 'Coming Soon', 'dinner': 'Coming Soon'},
            'Wednesday': {'breakfast': 'Coming Soon', 'lunch': 'Coming Soon', 'snacks': 'Coming Soon', 'dinner': 'Coming Soon'},
            'Thursday': {'breakfast': 'Coming Soon', 'lunch': 'Coming Soon', 'snacks': 'Coming Soon', 'dinner': 'Coming Soon'},
            'Friday': {'breakfast': 'Coming Soon', 'lunch': 'Coming Soon', 'snacks': 'Coming Soon', 'dinner': 'Coming Soon'},
            'Saturday': {'breakfast': 'Coming Soon', 'lunch': 'Coming Soon', 'snacks': 'Coming Soon', 'dinner': 'Coming Soon'},
            'Sunday': {'breakfast': 'Coming Soon', 'lunch': 'Coming Soon', 'snacks': 'Coming Soon', 'dinner': 'Coming Soon'}
        }
    else:
        weekly_menu = {m.day: {'breakfast': m.breakfast, 'lunch': m.lunch, 'snacks': m.snacks, 'dinner': m.dinner} for m in menus}
    
    # Get current day string, e.g., 'Friday'
    today_str = datetime.now().strftime('%A')
    
    return render_template('student/food_menu.html', weekly_menu=weekly_menu, today_str=today_str)


@student_bp.route('/profile')
@login_required
def profile():
    if current_user.role != 'student':
        abort(403)
    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    return render_template('student/profile.html', profile=profile)

@student_bp.route('/marks-cards', methods=['GET'])
@login_required
def marks_cards():
    if current_user.role != 'student':
        abort(403)
    cards = MarksCard.query.filter_by(user_id=current_user.id).all()
    timeline = MarksTimeline.query.filter_by(user_id=current_user.id).limit(10).all()
    cards_by_sem = {card.semester: card for card in cards}
    return render_template('student/marks_cards.html', cards=cards_by_sem, timeline=timeline)

@student_bp.route('/marks-cards/upload/<int:sem>', methods=['POST'])
@login_required
def upload_marks_card(sem):
    if current_user.role != 'student':
        abort(403)
        
    if 'file' not in request.files:
        flash('No file provided', 'danger')
        return redirect(url_for('student.marks_cards'))
        
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('student.marks_cards'))
        
    if file:
        filename = secure_filename(f"user_{current_user.id}_sem_{sem}_{file.filename}")
        upload_path = os.path.join(current_app.root_path, 'static', 'uploads', 'marks_cards')
        os.makedirs(upload_path, exist_ok=True)
        file_path_full = os.path.join(upload_path, filename)
        file.save(file_path_full)
        
        # Auto-verify with OCR
        with open(file_path_full, 'rb') as f:
            is_valid, ocr_msg, extracted_cgpa = verify_marks_card_ocr(f, sem)
        
        card = MarksCard.query.filter_by(user_id=current_user.id, semester=sem).first()
        
        new_status = 'Verified' if is_valid else 'Pending'
        
        if not is_valid:
            from app.models.notification import Notification
            student_name = current_user.student_profile.full_name if current_user.student_profile else "Student"
            notif = Notification(
                title="Document Verification Failed",
                description=f"{student_name}'s Marks Card (Semester {sem}) failed automated OCR verification.",
                category="Hostel",
                priority="High",
                target_user_id=current_user.id,
                target_role="warden"
            )
            db.session.add(notif)
            
        if card:
            card.file_path = filename
            card.status = new_status
            card.extracted_cgpa = extracted_cgpa
            card.admin_notes = ocr_msg
            card.updated_at = datetime.utcnow()
            log = MarksTimeline(user_id=current_user.id, title=f"Sem {sem} Re-uploaded", description=f"New version added. Status: {new_status}", status_type="success" if is_valid else "warning")
            db.session.add(log)
        else:
            card = MarksCard(user_id=current_user.id, semester=sem, file_path=filename, status=new_status, extracted_cgpa=extracted_cgpa, admin_notes=ocr_msg)
            db.session.add(card)
            log = MarksTimeline(user_id=current_user.id, title=f"Sem {sem} Uploaded", description=f"Document submitted. Status: {new_status}", status_type="success" if is_valid else "warning")
            db.session.add(log)
            
        db.session.commit()
        flash(f'Semester {sem} marks card uploaded successfully.', 'success')
        
    return redirect(url_for('student.marks_cards'))
        
@student_bp.route('/marks-cards/view/<filename>')
@login_required
def view_marks_card(filename):
    if current_user.role != 'student':
        abort(403)
    if not filename.startswith(f"user_{current_user.id}_"):
        abort(403)
    upload_path = os.path.join(current_app.root_path, 'static', 'uploads', 'marks_cards')
    return send_from_directory(upload_path, filename)

@student_bp.route('/complaints', methods=['GET', 'POST'])
@login_required
def complaints():
    from app.models.complaint import Complaint
    if current_user.role != 'student':
        abort(403)
        
    if request.method == 'POST':
        category = request.form.get('category')
        description = request.form.get('description')
        
        file = request.files.get('image')
        filename = None
        if file and file.filename != '':
            filename = secure_filename(f"complaint_{current_user.id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{file.filename}")
            upload_path = os.path.join(current_app.root_path, 'static', 'uploads', 'complaints')
            os.makedirs(upload_path, exist_ok=True)
            file.save(os.path.join(upload_path, filename))
            
        complaint = Complaint(
            user_id=current_user.id,
            category=category,
            description=description,
            image_path=filename
        )
        db.session.add(complaint)
        db.session.commit()
        flash('Your complaint has been submitted successfully.', 'success')
        return redirect(url_for('student.complaints'))
        
    history = Complaint.query.filter_by(user_id=current_user.id).all()
    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    return render_template('student/complaints.html', history=history, profile=profile)

@student_bp.route('/notifications')
@login_required
def notifications():
    from app.models.notification import Notification
    from sqlalchemy import or_, and_
    if current_user.role != 'student':
        abort(403)
        
    category_filter = request.args.get('category', 'All')
    
    base_query = Notification.query.filter(
        or_(
            Notification.target_user_id == current_user.id,
            Notification.target_role == 'student',
            and_(Notification.target_user_id == None, Notification.target_role == None)
        )
    )
    
    if category_filter == 'All':
        notices = base_query.order_by(Notification.created_at.desc()).all()
    else:
        notices = base_query.filter_by(category=category_filter).order_by(Notification.created_at.desc()).all()
        
    return render_template('student/notifications.html', notices=notices, current_category=category_filter)
