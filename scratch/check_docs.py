import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import db, StudentProfile, StaffProfile

app = create_app()

def validate_aadhaar(aadhaar_number):
    if not aadhaar_number:
        return False
    return aadhaar_number.isdigit() and len(aadhaar_number) == 12

def validate_ration_card(ration_number):
    if not ration_number:
        return False
    # Simple check: alphanumeric and reasonable length
    return ration_number.isalnum() and len(ration_number) >= 8

def main():
    with app.app_context():
        print("--- Checking Student Profiles ---")
        students = StudentProfile.query.all()
        invalid_aadhaar = []
        invalid_ration = []
        for s in students:
            if not validate_aadhaar(s.aadhaar_number):
                invalid_aadhaar.append((s.id, s.full_name, s.aadhaar_number))
            if not validate_ration_card(s.ration_card_number):
                invalid_ration.append((s.id, s.full_name, s.ration_card_number))
        
        print(f"Total students: {len(students)}")
        print(f"Invalid Aadhaar Numbers ({len(invalid_aadhaar)}):")
        for i in invalid_aadhaar:
            print(f"  ID: {i[0]}, Name: {i[1]}, Aadhaar: {i[2]}")
            
        print(f"Invalid Ration Card Numbers ({len(invalid_ration)}):")
        for i in invalid_ration:
            print(f"  ID: {i[0]}, Name: {i[1]}, Ration: {i[2]}")

if __name__ == "__main__":
    main()
