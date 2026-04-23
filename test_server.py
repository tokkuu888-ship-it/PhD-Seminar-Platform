#!/usr/bin/env python3
"""
Simple test to verify Flask server is working
"""

from app import app

def test_routes():
    with app.app_context():
        # Test if routes exist
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append(rule.rule)
        
        print("Available routes:")
        for route in sorted(routes):
            print(f"  {route}")
        
        # Check specific routes
        required_routes = ['/login', '/profile', '/']
        for route in required_routes:
            if route in routes:
                print(f"✅ {route} - Found")
            else:
                print(f"❌ {route} - Missing")

if __name__ == '__main__':
    test_routes()
