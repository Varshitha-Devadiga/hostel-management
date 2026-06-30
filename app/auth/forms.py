from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    PasswordField, 
    SelectField, 
    BooleanField, 
    RadioField, 
    TextAreaField, 
    IntegerField, 
    SelectMultipleField
)
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp, Length, Optional
from flask_wtf.file import FileField, FileRequired

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "Email", "class": "form-control", "autocomplete": "off"})
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={"placeholder": "Password", "class": "form-control", "autocomplete": "new-password"})
    remember = BooleanField('Remember Me')


class StudentRegistrationForm(FlaskForm):
    # ---- Auth fields -------------------------------------------------
    email = StringField('Email', validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "Email", "class": "form-control"})
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={"placeholder": "Password", "class": "form-control"})
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password', message='Passwords must match')],
                                     render_kw={"placeholder": "Confirm Password", "class": "form-control"})

    # ---- Personal info -----------------------------------------------
    full_name = StringField('Full Name', validators=[DataRequired()], render_kw={"class": "form-control"})
    dob = DateField('Date of Birth', validators=[DataRequired()], format='%Y-%m-%d', render_kw={"class": "form-control"})
    mobile = StringField('Mobile Number',
                         validators=[DataRequired(), Regexp(r'^\d{10}$', message="Must be a valid 10-digit mobile number.")],
                         render_kw={"class": "form-control", "placeholder": "10-digit mobile"})
    permanent_address = TextAreaField('Permanent Address', render_kw={"class": "form-control", "rows": "3"})
    photo = FileField('Passport Photo')

    # ---- Guardian info -----------------------------------------------
    father_name = StringField("Father's Name", validators=[DataRequired()], render_kw={"class": "form-control"})
    mother_name = StringField("Mother's Name", validators=[DataRequired()], render_kw={"class": "form-control"})
    guardian_mobile = StringField('Parent Mobile Number',
                                  validators=[DataRequired(), Regexp(r'^\d{10}$', message="Must be a valid 10-digit mobile number.")],
                                  render_kw={"class": "form-control", "placeholder": "10-digit mobile"})
    emergency_contact = StringField('Guardian Number',
                                    validators=[Optional(), Regexp(r'^\d{10}$', message="Must be a valid 10-digit phone number.")],
                                    render_kw={"class": "form-control", "placeholder": "10-digit phone"})

    # ---- College info ------------------------------------------------
    college = StringField('College Name', validators=[DataRequired()], render_kw={"class": "form-control", "list": "college-options", "placeholder": "Select or type college name"})
    university = StringField('Place', validators=[DataRequired()], render_kw={"class": "form-control", "list": "place-options", "placeholder": "Enter Place"})
    course = StringField('Course',
                         validators=[DataRequired()], 
                         render_kw={"class": "form-control", "list": "course-options", "placeholder": "Select or type course"})
    semester = SelectField('Semester',
                           choices=[('1', '1st Semester'), ('2', '2nd Semester'), ('3', '3rd Semester'), 
                                    ('4', '4th Semester'), ('5', '5th Semester'), ('6', '6th Semester'),
                                    ('7', '7th Semester'), ('8', '8th Semester'), ('9', '9th Semester'),
                                    ('10', '10th Semester')],
                           validators=[DataRequired()], render_kw={"class": "form-control"})
    admission_year = IntegerField('Admission Year', validators=[DataRequired()], render_kw={"class": "form-control"})
    course_duration = SelectField('Course Duration', choices=[('1', '1 Year'), ('2', '2 Years'), ('3', '3 Years'), ('4', '4 Years'), ('5', '5 Years'), ('6', '6 Years')], validators=[DataRequired()], render_kw={"class": "form-control"})
    completion_year = IntegerField('Expected Completion Year', validators=[Optional()], render_kw={"class": "form-control", "placeholder": "Auto-calculated", "readonly": True})
    hod_name = StringField('HOD Name', render_kw={"class": "form-control"})
    hod_phone = StringField('HOD Phone Number',
                            validators=[DataRequired(), Regexp(r'^\d{10}$', message="Must be a valid 10-digit phone number.")],
                            render_kw={"class": "form-control", "placeholder": "10-digit phone"})

    # ---- Food preferences --------------------------------------------
    diet = RadioField('Diet', choices=[('veg', 'Vegetarian'), ('non-veg', 'Non-Vegetarian')], validators=[DataRequired()], render_kw={"class": "form-control"})
    food_items = SelectMultipleField('Food Items', choices=[('egg', 'Egg'), ('chicken', 'Chicken'), ('fish', 'Fish')], render_kw={"class": "form-control"})

    # ---- Document uploads and numbers --------------------------------
    aadhaar_number = StringField('Aadhaar Number', 
                                 validators=[DataRequired(), Regexp(r'^\d{4}\s?\d{4}\s?\d{4}$', message="Aadhaar must be exactly 12 digits.")],
                                 render_kw={"class": "form-control", "placeholder": "XXXX XXXX XXXX", "maxlength": "14"})
    aadhaar = FileField('Aadhaar Card', validators=[FileRequired(message='Please upload your Aadhaar Card.')])
    
    ration_card_number = StringField('Ration Card Number',
                                     validators=[DataRequired()],
                                     render_kw={"class": "form-control", "placeholder": "Enter Ration Card Number"})
    ration_card = FileField('Ration Card', validators=[FileRequired(message='Please upload your Ration Card.')])
    
    college_id = FileField('College ID')
    ssp_id = StringField('SSP ID', render_kw={"class": "form-control"})
    food_preference = StringField('Food Preference', render_kw={"class": "form-control"})
    
    agree = BooleanField('I agree to terms and conditions', validators=[DataRequired()])