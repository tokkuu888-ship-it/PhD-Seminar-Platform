#!/usr/bin/env python3
"""
PhD Seminar Platform Startup Script
This script starts the Flask application with ngrok tunneling for remote access.
"""

import sys
import os
from app import app, db, create_default_users
import pyngrok
from pyngrok import ngrok

def main():
    print("=" * 60)
    print("PhD Seminar Platform Starting...")
    print("=" * 60)
    
    # Initialize database
    with app.app_context():
        try:
            db.create_all()
            create_default_users()
            print("✓ Database initialized successfully")
        except Exception as e:
            print(f"✗ Database initialization failed: {e}")
            return
    
    # Configure ngrok
    NGROK_AUTHTOKEN = "YOUR_NGROK_AUTHTOKEN_HERE"
    
    if NGROK_AUTHTOKEN != "YOUR_NGROK_AUTHTOKEN_HERE":
        try:
            ngrok.set_auth_token(NGROK_AUTHTOKEN)
            print("✓ Ngrok authentication configured")
        except Exception as e:
            print(f"⚠ Ngrok authentication failed: {e}")
            print("  Please update your ngrok authtoken in the .env file or app.py")
    else:
        print("⚠ Ngrok authtoken not configured")
        print("  To enable remote access, update your ngrok authtoken:")
        print("  1. Get your authtoken from https://dashboard.ngrok.com/auth")
        print("  2. Update the .env file or app.py with your authtoken")
    
    # Start ngrok tunnel
    try:
        print("🚀 Starting ngrok tunnel...")
        ngrok_tunnel = ngrok.connect(5000)
        public_url = ngrok_tunnel.public_url
        print(f"✓ Ngrok tunnel established: {public_url}")
    except Exception as e:
        print(f"⚠ Failed to start ngrok tunnel: {e}")
        print("  Running in local mode only")
        public_url = "http://localhost:5000"
    
    print("\n" + "=" * 60)
    print("PLATFORM ACCESS URLs:")
    print("=" * 60)
    print(f"📱 Mobile/Desktop Access: {public_url}")
    print(f"🏠 Local Access:        http://localhost:5000")
    print("=" * 60)
    
    print("\n📋 Demo Accounts:")
    print("┌─────────────┬──────────────┬─────────────┐")
    print("│    Role     │   Username   │   Password  │")
    print("├─────────────┼──────────────┼─────────────┤")
    print("│    Dean     │     dean     │  admin123   │")
    print("│  Professor  │  professor1  │   prof123   │")
    print("│ PhD Candidate│   student1   │ student123  │")
    print("└─────────────┴──────────────┴─────────────┘")
    
    print("\n🚀 Starting Flask web server...")
    print("   Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        app.run(debug=False, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"✗ Server error: {e}")
    finally:
        # Clean up ngrok tunnel
        try:
            ngrok.disconnect(public_url)
            print("✓ Ngrok tunnel closed")
        except:
            pass

if __name__ == '__main__':
    main()
