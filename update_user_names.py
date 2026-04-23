#!/usr/bin/env python3
"""
Script to update professor and student names in database
"""

from app import app, db, User

def update_user_names():
    with app.app_context():
        # Update professor name
        professor = User.query.filter_by(username='professor1').first()
        if professor:
            print(f"Current professor name: {professor.full_name}")
            professor.full_name = 'Professor Dereje Hailu'
            db.session.commit()
            print(f"Updated professor name to: {professor.full_name}")
        else:
            print("Professor user not found!")
        
        # Update student name
        student = User.query.filter_by(username='student1').first()
        if student:
            print(f"Current student name: {student.full_name}")
            student.full_name = 'Tokuma Adamu'
            db.session.commit()
            print(f"Updated student name to: {student.full_name}")
        else:
            print("Student user not found!")
        
        print("\n✅ All user names updated successfully!")

if __name__ == '__main__':
    update_user_names()
