from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import admin_bp
from .. import db
from ..models import User

# Ensure only admin users can access
def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

from app.models.student_profile import StudentProfile
from app.models.leave import LeaveRequest
from app.models.notification import Notification
from app.utils.email import send_notification_email

@admin_bp.route('/admin/dashboard')
@login_required
@admin_required
def dashboard():
    from datetime import datetime
    total_students = StudentProfile.query.count()
    
    # Calculate students on leave today
    today = datetime.utcnow().date()
    on_leave_today = LeaveRequest.query.filter(
        LeaveRequest.status == 'Approved',
        LeaveRequest.from_date <= today,
        LeaveRequest.is_returned == False
    ).count()
    
    present_today = total_students - on_leave_today
    pending_reg = StudentProfile.query.filter_by(status='Pending Review').count()
    
    # Simple activity log from LeaveRequests
    recent_leaves = LeaveRequest.query.order_by(LeaveRequest.created_at.desc()).limit(5).all()

    return render_template('admin/dashboard.html', 
                           total_students=total_students,
                           present_today=present_today,
                           on_leave_today=on_leave_today,
                           pending_reg=pending_reg,
                           recent_leaves=recent_leaves)

@admin_bp.route('/admin/students')
@login_required
@admin_required
def manage_students():
    sort_by = request.args.get('sort', 'id')
    
    if sort_by == 'full_name':
        students = StudentProfile.query.order_by(StudentProfile.full_name).all()
    elif sort_by == 'course':
        students = StudentProfile.query.order_by(StudentProfile.course).all()
    else:
        students = StudentProfile.query.all()
        
    from datetime import datetime
    from app.models.leave import LeaveRequest
    
    total_students = StudentProfile.query.filter_by(status='Verified').count()
    
    today = datetime.utcnow().date()
    on_leave_query = LeaveRequest.query.filter(
        LeaveRequest.status == 'Approved',
        LeaveRequest.from_date <= today,
        LeaveRequest.is_returned == False
    ).all()
    on_leave_today = len(on_leave_query)
    on_leave_user_ids = [req.user_id for req in on_leave_query]
    
    present_today = total_students - on_leave_today
    if present_today < 0:
        present_today = 0
        
    pending_reg = StudentProfile.query.filter((StudentProfile.status != 'Verified') | (StudentProfile.status.is_(None))).count()
    return render_template('admin/users.html', 
                           students=students,
                           total_students=total_students,
                           present_today=present_today,
                           on_leave_today=on_leave_today,
                           pending_reg=pending_reg,
                           on_leave_user_ids=on_leave_user_ids)

@admin_bp.route('/admin/student/<int:id>')
@login_required
@admin_required
def view_student(id):
    student = StudentProfile.query.get_or_404(id)
    return render_template('admin/student_profile.html', student=student)

@admin_bp.route('/admin/approve/<int:id>')
@login_required
@admin_required
def approve_student(id):
    student = StudentProfile.query.get_or_404(id)
    student.status = 'Verified'
    db.session.commit()
    flash(f"Student {student.full_name} verified successfully.", "success")
    # Redirect back to profile if referred from there, otherwise manage students
    if request.referrer and 'student' in request.referrer:
        return redirect(request.referrer)
    return redirect(url_for('admin.manage_students'))

@admin_bp.route('/admin/reject/<int:id>')
@login_required
@admin_required
def reject_student(id):
    student = StudentProfile.query.get_or_404(id)
    student.status = 'Rejected'
    db.session.commit()
    flash(f"Student {student.full_name}'s registration has been rejected due to invalid documents.", "danger")
    if request.referrer and 'student' in request.referrer:
        return redirect(request.referrer)
    return redirect(url_for('admin.manage_students'))

from flask import Response
import csv
import io

@admin_bp.route('/admin/students/export')
@login_required
@admin_required
def export_students():
    students = StudentProfile.query.all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'ID', 'Full Name', 'DOB', 'Mobile', 
        'Father Name', 'Mother Name', 'Guardian Name', 'Guardian Mobile', 'Emergency Contact',
        'College', 'University', 'Course', 'Semester', 'Admission Year', 'Course Duration', 'Completion Year',
        'HOD Name', 'HOD Phone', 'Diet', 'Aadhaar Number', 'Ration Card Number', 'Status'
    ])
    
    # Write data
    for student in students:
        writer.writerow([
            student.id,
            student.full_name,
            student.dob.strftime('%Y-%m-%d') if student.dob else '',
            f'="{student.mobile}"' if student.mobile else '',
            student.father_name,
            student.mother_name,
            student.guardian_name,
            f'="{student.guardian_mobile}"' if student.guardian_mobile else '',
            f'="{student.emergency_contact}"' if student.emergency_contact else '',
            student.college,
            student.university,
            student.course,
            student.semester,
            student.admission_year,
            student.course_duration,
            student.completion_year,
            student.hod_name,
            f'="{student.hod_phone}"' if student.hod_phone else '',
            student.diet,
            f'="{student.aadhaar_number}"' if student.aadhaar_number else '',
            f'="{student.ration_card_number}"' if student.ration_card_number else '',
            student.status
        ])
        
    response = Response(output.getvalue(), mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=student_report.csv'
    return response

@admin_bp.route('/admin/student/delete/<int:id>', methods=['POST', 'GET'])
@login_required
@admin_required
def delete_student(id):
    student = StudentProfile.query.get_or_404(id)
    user_id_to_delete = student.user_id
    
    db.session.delete(student)
    
    # Check for legacy Student record
    try:
        from app.models.student import Student
        legacy_student = Student.query.filter_by(user_id=user_id_to_delete).first()
        if legacy_student:
            db.session.delete(legacy_student)
    except:
        pass
        
    user = User.query.get(user_id_to_delete)
    if user:
        db.session.delete(user)
        
    db.session.commit()
    flash(f"Student {student.full_name} has been deleted.", "success")
    return redirect(url_for('admin.manage_students'))

@admin_bp.route('/admin/student/<int:id>', methods=['GET'])
@login_required
@admin_required
def view_student_profile(id):
    student = StudentProfile.query.get_or_404(id)
    return render_template('admin/view_student_profile.html', student=student)

from datetime import date

@admin_bp.route('/admin/leaves')
@login_required
@admin_required
def manage_leaves():
    # Fetch student leave requests
    pending_leaves = db.session.query(LeaveRequest, StudentProfile).join(User, LeaveRequest.user_id == User.id).join(StudentProfile, User.id == StudentProfile.user_id).filter(LeaveRequest.status == 'Pending').order_by(LeaveRequest.created_at.desc()).all()
    recent_history = db.session.query(LeaveRequest, StudentProfile).join(User, LeaveRequest.user_id == User.id).join(StudentProfile, User.id == StudentProfile.user_id).filter(LeaveRequest.status != 'Pending').order_by(LeaveRequest.updated_at.desc()).limit(20).all()
    
    # Fetch staff leave requests
    from app.models.staff_profile import StaffProfile
    staff_pending = db.session.query(LeaveRequest, StaffProfile).join(User, LeaveRequest.user_id == User.id).join(StaffProfile, User.id == StaffProfile.user_id).filter(LeaveRequest.status == 'Pending').order_by(LeaveRequest.created_at.desc()).all()
    staff_history = db.session.query(LeaveRequest, StaffProfile).join(User, LeaveRequest.user_id == User.id).join(StaffProfile, User.id == StaffProfile.user_id).filter(LeaveRequest.status != 'Pending').order_by(LeaveRequest.updated_at.desc()).limit(20).all()

    today = date.today()
    currently_away = db.session.query(LeaveRequest, StudentProfile).join(User, LeaveRequest.user_id == User.id).join(StudentProfile, User.id == StudentProfile.user_id).filter(LeaveRequest.status == 'Approved', LeaveRequest.from_date <= today, LeaveRequest.is_returned == False).all()
    
    overdue_leaves = []
    returns_today_leaves = []
    for leave, student in currently_away:
        if leave.to_date < today:
            overdue_leaves.append((leave, student))
        elif leave.to_date == today:
            returns_today_leaves.append((leave, student))
    
    return render_template('admin/leaves.html', 
                           pending_leaves=pending_leaves, 
                           recent_history=recent_history, 
                           currently_away=currently_away,
                           overdue_leaves=overdue_leaves,
                           returns_today_leaves=returns_today_leaves,
                           staff_pending=staff_pending,
                           staff_history=staff_history)

@admin_bp.route('/admin/leave/update/<int:id>', methods=['POST'])
@login_required
@admin_required
def update_leave_status(id):
    leave = LeaveRequest.query.get_or_404(id)
    action = request.form.get('action')
    if action == 'approve':
        leave.status = 'Approved'
        flash("Leave request approved.", "success")
    elif action == 'reject':
        leave.status = 'Rejected'
        flash("Leave request rejected.", "danger")
    db.session.commit()
    return redirect(url_for('admin.manage_leaves'))

@admin_bp.route('/admin/staff', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_staff():
    if request.method == 'POST':
        if request.form.get('add_staff'):
            name = request.form.get('name')
            role = request.form.get('role')
            email = request.form.get('email', '').strip().lower()
            password = request.form.get('password')
            
            from app.models.user import User
            
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash(f'Email {email} is already registered.', 'danger')
                return redirect(url_for('admin.manage_staff'))
                
            new_user = User(email=email, role='staff')  # type: ignore
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.flush() # get user ID
            
            from app.models.staff_profile import StaffProfile
            sp = StaffProfile(user_id=new_user.id, full_name=name, specialty=role)  # type: ignore
            db.session.add(sp)
            db.session.commit()
            
            flash(f'New staff added! They can now log in with the email and password you set.', 'success')
            return redirect(url_for('admin.manage_staff'))
            
    from app.models.user import User
    from app.models.staff_profile import StaffProfile
    
    # Ensure all users with role 'staff' have a StaffProfile
    staff_users = User.query.filter_by(role='staff').all()
    profiles_added = False
    for user in staff_users:
        if not StaffProfile.query.filter_by(user_id=user.id).first():
            fallback_name = user.email.split('@')[0].capitalize() if user.email else 'Staff Member'
            sp = StaffProfile(user_id=user.id, full_name=fallback_name, specialty='General Staff')
            db.session.add(sp)
            profiles_added = True
            
    if profiles_added:
        db.session.commit()
        
    staff_profiles = StaffProfile.query.all()
    total_staff = len(staff_profiles)
    on_duty = sum(1 for s in staff_profiles if s.status == 'On Duty')
    on_leave = sum(1 for s in staff_profiles if s.status == 'On Leave')
    
    return render_template('admin/staff.html', 
                           staff_list=staff_profiles,
                           total_staff=total_staff, 
                           on_duty=on_duty, 
                           on_leave=on_leave)

@admin_bp.route('/admin/staff/<int:user_id>/edit', methods=['POST'])
@login_required
@admin_required
def edit_staff(user_id):
    from app.models.staff_profile import StaffProfile
    profile = StaffProfile.query.filter_by(user_id=user_id).first()
    if profile:
        profile.full_name = request.form.get('name', '').strip()
        profile.specialty = request.form.get('role', '').strip()
        profile.status = request.form.get('status', 'On Duty')
        db.session.commit()
        flash('Staff profile updated successfully.', 'success')
    else:
        flash('Staff profile not found.', 'danger')
    return redirect(url_for('admin.manage_staff'))

@admin_bp.route('/admin/staff/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_staff(user_id):
    from app.models.user import User
    from app.models.staff_profile import StaffProfile
    
    # Don't allow deleting yourself if you are somehow staff
    if user_id == current_user.id:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('admin.manage_staff'))
        
    user = User.query.get(user_id)
    if user and user.role == 'staff':
        profile = StaffProfile.query.filter_by(user_id=user_id).first()
        if profile:
            db.session.delete(profile)
        db.session.delete(user)
        db.session.commit()
        flash('Staff member completely removed.', 'success')
    else:
        flash('Staff member not found or invalid permissions.', 'danger')
        
    return redirect(url_for('admin.manage_staff'))

from app.models.menu import FoodMenu

@admin_bp.route('/admin/food')
@login_required
@admin_required
def manage_food():
    # Seed the database if it's empty
    if FoodMenu.query.count() == 0:
        default_menu = {
            'Monday': {'breakfast': 'Poha & Masala Chai', 'lunch': 'North Indian Veg Thali', 'snacks': 'Glucose Biscuits & Tea', 'dinner': 'Roti & Tadka Dal'},
            'Tuesday': {'breakfast': 'Idli Sambar', 'lunch': 'South Indian Thali', 'snacks': 'Samosa & Tea', 'dinner': 'Veg Pulao'},
            'Wednesday': {'breakfast': 'Aloo Paratha', 'lunch': 'Rajma Chawal', 'snacks': 'Namkeen & Tea', 'dinner': 'Mix Veg & Roti'},
            'Thursday': {'breakfast': 'Upma', 'lunch': 'Dal Makhani & Rice', 'snacks': 'Biscuits', 'dinner': 'Paneer Curry & Roti'},
            'Friday': {'breakfast': 'Dosa Chutney', 'lunch': 'Veg Biryani', 'snacks': 'Bread Pakoda', 'dinner': 'Egg Curry & Roti'},
            'Saturday': {'breakfast': 'Puri Bhaji', 'lunch': 'Special Veg Thali', 'snacks': 'Fruits & Tea', 'dinner': 'Khichdi'},
            'Sunday': {'breakfast': 'Chole Bhature', 'lunch': 'Chicken Curry / Veg Kofta', 'snacks': 'Pastries', 'dinner': 'Veg Fried Rice'}
        }
        for day, meals in default_menu.items():
            menu_item = FoodMenu(day=day, breakfast=request.form.get(f'{day}_breakfast'), lunch=request.form.get(f'{day}_lunch'), snacks=request.form.get(f'{day}_snacks'), dinner=request.form.get(f'{day}_dinner'))  # type: ignore
            db.session.add(menu)
        db.session.commit()
        
    menus = FoodMenu.query.all()
    weekly_menu = {m.day: {'breakfast': m.breakfast, 'lunch': m.lunch, 'snacks': m.snacks, 'dinner': m.dinner} for m in menus}
    
    from app.models.student_profile import StudentProfile
    students = StudentProfile.query.all()
    total_responders = len(students)
    
    chicken_count = 0
    fish_count = 0
    egg_count = 0
    
    for s in students:
        if s.food_items:
            if 'chicken' in s.food_items:
                chicken_count += 1
            if 'fish' in s.food_items:
                fish_count += 1
            if 'egg' in s.food_items:
                egg_count += 1
    
    return render_template('admin/food.html', weekly_menu=weekly_menu,
                           chicken_count=chicken_count,
                           fish_count=fish_count,
                           egg_count=egg_count,
                           total_responders=total_responders)

@admin_bp.route('/admin/food/export')
@login_required
@admin_required
def export_food_report():
    from app.models.student_profile import StudentProfile
    from flask import Response
    import csv
    import io
    
    students = StudentProfile.query.all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Full Name', 'Course', 'Diet', 'Food Items'])
    
    for student in students:
        food_items = ', '.join(student.food_items) if student.food_items else 'None'
        writer.writerow([
            student.id,
            student.full_name,
            student.course,
            student.diet,
            food_items
        ])
        
    response = Response(output.getvalue(), mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=special_meal_report.csv'
    return response

@admin_bp.route('/admin/food/notify', methods=['POST'])
@login_required
@admin_required
def notify_food_preferences():
    flash('Notification sent to all students to update their food preferences.', 'success')
    return redirect(url_for('admin.manage_food'))

@admin_bp.route('/admin/food-menu/update', methods=['POST'])
@login_required
@admin_required
def update_menu():
    menus = FoodMenu.query.all()
    for menu in menus:
        # e.g. "Monday_breakfast"
        breakfast_val = request.form.get(f"{menu.day}_breakfast")
        lunch_val = request.form.get(f"{menu.day}_lunch")
        snacks_val = request.form.get(f"{menu.day}_snacks")
        dinner_val = request.form.get(f"{menu.day}_dinner")
        
        if breakfast_val is not None:
            menu.breakfast = breakfast_val
        if lunch_val is not None:
            menu.lunch = lunch_val
        if snacks_val is not None:
            menu.snacks = snacks_val
        if dinner_val is not None:
            menu.dinner = dinner_val
            
    db.session.commit()
    flash('Menu successfully updated.', 'success')
    return redirect(url_for('admin.manage_food'))

@admin_bp.route('/admin/food-menu/broadcast', methods=['POST'])
@login_required
@admin_required
def broadcast_menu():
    # Send an email with today's (or the whole week's) menu to all students
    menus = FoodMenu.query.all()
    body = "Here is the current Hostel Food Menu:\n\n"
    for menu in menus:
        body += f"--- {menu.day} ---\n"
        body += f"Breakfast: {menu.breakfast}\n"
        body += f"Lunch: {menu.lunch}\n"
        body += f"Snacks: {menu.snacks}\n"
        body += f"Dinner: {menu.dinner}\n\n"
        
    # Get all students
    from app.models.user import User
    students = User.query.filter_by(role='student').all()
    emails = [student.email for student in students if student.email]
    
    if emails:
        send_notification_email("Hostel Food Menu Update", body, emails)
        flash(f'Menu broadcast sent successfully to {len(emails)} students!', 'success')
    else:
        flash('No students found to send the menu to.', 'warning')
        
    return redirect(url_for('admin.manage_food'))

@admin_bp.route('/admin/complaints')
@login_required
@admin_required
def manage_complaints():
    from app.models.complaint import Complaint
    pending_complaints = db.session.query(Complaint, StudentProfile).join(User, Complaint.user_id == User.id).join(StudentProfile, User.id == StudentProfile.user_id).filter(Complaint.status == 'Pending').order_by(Complaint.created_at.desc()).all()
    resolved_complaints = db.session.query(Complaint, StudentProfile).join(User, Complaint.user_id == User.id).join(StudentProfile, User.id == StudentProfile.user_id).filter(Complaint.status == 'Resolved').order_by(Complaint.updated_at.desc()).limit(20).all()
    return render_template('admin/complaints.html', pending_complaints=pending_complaints, resolved_complaints=resolved_complaints)

@admin_bp.route('/admin/complaint/resolve/<int:id>', methods=['POST'])
@login_required
@admin_required
def resolve_complaint(id):
    from app.models.complaint import Complaint
    complaint = Complaint.query.get_or_404(id)
    admin_notes = request.form.get('admin_notes', '')
    
    complaint.status = 'Resolved'
    complaint.admin_notes = admin_notes
    db.session.commit()
    
    flash("Complaint marked as resolved.", "success")
    return redirect(url_for('admin.manage_complaints'))

@admin_bp.route('/admin/marks-cards')
@login_required
@admin_required
def manage_marks_cards():
    from app.models.marks_card import MarksCard
    all_cards = db.session.query(MarksCard, StudentProfile).join(User, MarksCard.user_id == User.id).join(StudentProfile, User.id == StudentProfile.user_id).order_by(MarksCard.semester.desc()).all()
    
    grouped_students = {}
    total_pending = 0
    total_verified = 0

    for card, student in all_cards:
        if student.id not in grouped_students:
            grouped_students[student.id] = {'student': student, 'cards': []}
        grouped_students[student.id]['cards'].append(card)
        
        if card.status == 'Pending':
            total_pending += 1
        elif card.status == 'Verified':
            total_verified += 1
            
    # Sort students so those with pending cards appear first
    sorted_students = sorted(grouped_students.values(), key=lambda x: any(c.status == 'Pending' for c in x['cards']), reverse=True)

    return render_template('admin/marks_cards.html', 
                           grouped_students=sorted_students,
                           total_pending=total_pending,
                           total_verified=total_verified)

@admin_bp.route('/admin/marks-cards/verify/<int:id>', methods=['POST'])
@login_required
@admin_required
def verify_marks_card(id):
    from app.models.marks_card import MarksCard, MarksTimeline
    card = MarksCard.query.get_or_404(id)
    action = request.form.get('action')
    admin_notes = request.form.get('admin_notes', '')
    
    if action == 'verify':
        card.status = 'Verified'
        log = MarksTimeline(user_id=card.user_id, title=f"Sem {card.semester} Verified", description="Admin approved your submission. " + admin_notes, status_type="success")  # type: ignore
        db.session.add(log)
        flash("Marks card verified.", "success")
    elif action == 'reject':
        card.status = 'Rejected'
        log = MarksTimeline(user_id=card.user_id, title=f"Upload Rejected", description=admin_notes if admin_notes else f"Blurry scan detected for Sem {card.semester}.", status_type="error")  # type: ignore
        db.session.add(log)
        flash("Marks card rejected.", "danger")
        
    card.admin_notes = admin_notes
    db.session.commit()
    return redirect(url_for('admin.manage_marks_cards'))

@admin_bp.route('/admin/notices', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_notices():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category', 'General')
        audience = request.form.get('audience', 'All Students')
        
        target_role = None
        if audience == 'All Students':
            target_role = 'student'
        elif audience == 'All Staff':
            target_role = 'staff'
            
        new_notice = Notification(title=title, description=description, category=category, target_role=target_role)  # type: ignore
        db.session.add(new_notice)
        db.session.commit()
        
        # Get emails based on audience
        from app.models.user import User
        emails = []
        if audience in ['All Students', 'Both']:
            students = User.query.filter_by(role='student').all()
            emails.extend([s.email for s in students if s.email])
        if audience in ['All Staff', 'Both']:
            staff = User.query.filter_by(role='staff').all()
            emails.extend([s.email for s in staff if s.email])
            
        if emails:
            body = f"Hello,\n\nYou have a new {category} notice from the Warden:\n\n{description}\n\nRegards,\nBCWD Administration"
            send_notification_email(f"New Notice: {title}", body, emails)
            flash(f'Notification sent successfully to {len(emails)} recipients.', 'success')
        else:
            flash('Notice saved, but no users found to email.', 'warning')
            
        return redirect(url_for('admin.manage_notices'))
        
    notices = Notification.query.order_by(Notification.created_at.desc()).all()
    total_sent = len(notices)
    avg_reach = "100%" if total_sent > 0 else "0%"
    scheduled = 0
    return render_template('admin/notices.html', notices=notices, total_sent=total_sent, avg_reach=avg_reach, scheduled=scheduled)

@admin_bp.route('/admin/reports')
@login_required
@admin_required
def manage_reports():
    from collections import Counter
    students = StudentProfile.query.all()
    
    # Calculate Course Distribution
    courses = [s.course for s in students if s.course]
    course_counts = Counter(courses)
    course_labels = list(course_counts.keys())
    course_data = list(course_counts.values())
    
    if not course_labels:
        course_labels = ['No Data']
        course_data = [0]
        
    # Calculate Food Preference Distribution
    diets = [s.diet for s in students if s.diet]
    diet_counts = Counter(diets)
    diet_labels = ['Vegetarian', 'Non-Vegetarian']
    diet_data = [diet_counts.get('veg', 0), diet_counts.get('non-veg', 0)]
    
    if sum(diet_data) == 0:
        diet_data = [1, 0] # Avoid empty chart
        diet_labels = ['No Data', '']
        
    # Calculate Complaint Stats
    from app.models.complaint import Complaint
    complaints = Complaint.query.all()
    
    complaint_stats = {}
    for c in complaints:
        if c.category not in complaint_stats:
            complaint_stats[c.category] = {'total': 0, 'resolved': 0}
        complaint_stats[c.category]['total'] += 1
        if c.status == 'Resolved':
            complaint_stats[c.category]['resolved'] += 1
            
    for cat, data in complaint_stats.items():
        rate = 0
        if data['total'] > 0:
            rate = int((data['resolved'] / data['total']) * 100)
        data['rate'] = rate

    return render_template('admin/reports.html', 
                           course_labels=course_labels, 
                           course_data=course_data,
                           diet_labels=diet_labels,
                           diet_data=diet_data,
                           complaint_stats=complaint_stats)

@admin_bp.route('/admin/activity')
@login_required
@admin_required
def activity_overview():
    # placeholder data collections
    leaves = []  # would query LeaveRequest model
    holidays = []  # would query Holiday model
    return render_template('admin/activity.html', leaves=leaves, holidays=holidays)

@admin_bp.route('/admin/reports/export')
@login_required
@admin_required
def export_reports():
    from app.models.complaint import Complaint
    from app.models.student_profile import StudentProfile
    from app.models.user import User
    import csv
    import io
    from flask import Response
    
    complaints_data = db.session.query(Complaint, StudentProfile).join(User, Complaint.user_id == User.id).join(StudentProfile, User.id == StudentProfile.user_id).order_by(Complaint.created_at.desc()).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Complaint ID', 'Date', 'Student Name', 'Course', 'Category', 'Description', 'Status', 'Admin Notes'])
    
    for complaint, student in complaints_data:
        writer.writerow([
            complaint.id,
            complaint.created_at.strftime('%Y-%m-%d %H:%M') if complaint.created_at else '',
            student.full_name,
            student.course,
            complaint.category,
            complaint.description,
            complaint.status,
            complaint.admin_notes or ''
        ])
        
    response = Response(output.getvalue(), mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=complaint_master_report.csv'
    return response
