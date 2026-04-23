#!/usr/bin/env python3
"""
Script to update dean's username in database
"""

from app import app, db, User

def update_dean_username():
    with app.app_context():
        # Find dean user by old username
        dean = User.query.filter_by(username='dr_yenesew_mengiste').first()
        
        if dean:
            print(f"Current dean username: {dean.username}")
            # Update username to something more professional
            dean.username = 'dr_yenesew_mengiste'
            db.session.commit()
            print(f"Updated dean username to: {dean.username}")
            print(f"Dean account updated successfully - Username is now: {dean.username}")
        else:
            print("Dean user not found!")

if __name__ == '__main__':
    update_dean_username()
