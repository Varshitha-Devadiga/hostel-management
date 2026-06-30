"""Models package initialisation. Import models for convenient access."""

# Core extensions (re-exported so other code can do `from app.models import db`)
from app import db, bcrypt

# Import only models that exist
from .user import User
from .student import Student
from .student_profile import StudentProfile
from .staff_profile import StaffProfile

# Future models — uncomment as you create them:
from .room import Room
from .leave import LeaveRequest
from .menu import FoodMenu
from .marks_card import MarksCard, MarksTimeline
from .complaint import Complaint
from .notification import Notification
from .meal_rsvp import MealRSVP
# from .attendance import Attendance
# from .holiday import Holiday
