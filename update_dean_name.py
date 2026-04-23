#!/usr/bin/env python3
"""
Script to update the dean's name in the existing database
"""

from app import app, db, User

def update_dean_name():
    with app.app_context():
        # Find the dean user
        dean = User.query.filter_by(username='dean').first()
        
        if dean:
            print(f"Current dean name: {dean.full_name}")
            # Update the name
            dean.full_name = 'Dr. Yenesew Mengiste'
            db.session.commit()
            print(f"Updated dean name to: {dean.full_name}")
        else:
            print("Dean user not found!")
            
        # Verify the update
        updated_dean = User.query.filter_by(username='dean').first()
        if updated_dean:
            print(f"Verified dean name: {updated_dean.full_name}")

if __name__ == '__main__':
    update_dean_name()
