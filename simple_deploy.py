#!/usr/bin/env python3
"""
Simple PhD Seminar Platform Deployment - Single Endpoint
"""

import os
import time
from flask import Flask
from app import app
import pyngrok
from pyngrok import ngrok

def simple_deploy():
    """Deploy with single ngrok endpoint to avoid pooling issues"""
    
    print("🚀 Starting Simple PhD Seminar Platform Deployment...")
    print("=" * 60)
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    ngrok_authtoken = os.getenv('NGROK_AUTHTOKEN')
    
    if not ngrok_authtoken or ngrok_authtoken == 'YOUR_NGROK_AUTHTOKEN_HERE':
        print("❌ Ngrok authtoken not configured!")
        return
    
    # Configure ngrok
    try:
        ngrok.set_auth_token(ngrok_authtoken)
        print("✅ Ngrok authentication successful")
    except Exception as e:
        print(f"❌ Ngrok authentication failed: {e}")
        return
    
    # Kill existing tunnels first
    try:
        ngrok.kill()
        time.sleep(2)
        print("🔄 Cleared existing ngrok tunnels")
    except:
        pass
    
    # Start single ngrok tunnel
    try:
        print("🌐 Starting ngrok tunnel...")
        
        # Create tunnel with specific config
        tunnel = ngrok.connect(
            addr="5000",
            proto="http",
            bind_tls=True,
            options={
                "bind_tls": True,
                "domain": None,  # Let ngrok generate random domain
                "addr": "5000"
            }
        )
        
        public_url = tunnel.public_url
        
        print("\n" + "=" * 60)
        print("🎉 DEPLOYMENT SUCCESSFUL!")
        print("=" * 60)
        print(f"🌍 Public URL: {public_url}")
        print(f"🏠 Local Access: http://localhost:5000")
        print(f"📱 Mobile Access: http://10.5.19.50:5000")
        print("=" * 60)
        
        print("\n📋 Demo Accounts:")
        print("┌─────────────┬──────────────┬─────────────┐")
        print("│    Role     │   Username   │   Password  │")
        print("├─────────────┼──────────────┼─────────────┤")
        print("│    Dean     │ dr_yenesew_  │  admin123   │")
        print("│             │ mengiste     │             │")
        print("│  Professor  │  professor1  │   prof123   │")
        print("│ PhD Candidate│   student1   │ student123  │")
        print("└─────────────┴──────────────┴─────────────┘")
        
        print(f"\n🎓 Dean Name: Dr. Yenesew Mengiste")
        print(f"👨‍🏫 Professor: Professor Dereje Hailu")
        print(f"👩‍🎓 Student: Tokuma Adamu")
        
        print("\n📱 Platform Features:")
        print("✅ User Registration (Students & Professors)")
        print("✅ Profile Editing")
        print("✅ Seminar Scheduling")
        print("✅ Progress Reports")
        print("✅ Feedback System")
        print("✅ Mobile & Desktop Compatible")
        
        print(f"\n🔗 Share this URL: {public_url}")
        print("📧 Anyone with the link can access the platform!")
        
        # Start Flask app
        print(f"\n🚀 Starting web server...")
        print("📝 Press Ctrl+C to stop the deployment")
        print("=" * 60)
        
        app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
        
    except Exception as e:
        print(f"❌ Failed to start ngrok tunnel: {e}")
        print("🏠 Running locally only at: http://localhost:5000")
        app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == '__main__':
    simple_deploy()
