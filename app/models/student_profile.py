from . import db

class StudentProfile(db.Model):
    __tablename__ = 'student_profile'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    # Guardian fields
    father_name = db.Column(db.String(120))
    mother_name = db.Column(db.String(120))
    guardian_name = db.Column(db.String(120))
    guardian_mobile = db.Column(db.String(20))
    emergency_contact = db.Column(db.String(20))
    # College fields
    college = db.Column(db.String(120))
    university = db.Column(db.String(120))
    course = db.Column(db.String(120))
    semester = db.Column(db.String(20))
    admission_year = db.Column(db.Integer)
    course_duration = db.Column(db.Integer)
    completion_year = db.Column(db.Integer)
    hod_name = db.Column(db.String(120))
    hod_phone = db.Column(db.String(20))
    # Food preferences
    diet = db.Column(db.Enum('veg', 'non-veg', name='diet_enum'), default='veg')
    food_items = db.Column(db.JSON)  # list of selected items
    # Document paths and numbers
    aadhaar_number = db.Column(db.String(12))
    aadhaar_path = db.Column(db.String(200))
    ration_card_number = db.Column(db.String(20))
    ration_card_path = db.Column(db.String(200))
    college_id_path = db.Column(db.String(200))
    agreed = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='Pending Review')

    from sqlalchemy.orm import validates
    @validates('full_name')
    def validate_full_name(self, key, value):
        return value.title() if value else value

    user = db.relationship('User', backref=db.backref('student_profile', uselist=False, cascade='all, delete-orphan'))
