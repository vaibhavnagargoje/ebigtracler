#!/usr/bin/env python
"""
Test script to verify Bug Tracker functionality
"""
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BugTracker.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse

def test_basic_functionality():
    """Test basic functionality of the Bug Tracker application"""
    print("Testing Bug Tracker Basic Functionality...")
    print("=" * 50)
    
    client = Client()
    
    # Test home page
    print("1. Testing home page...")
    try:
        response = client.get('/')
        if response.status_code == 200:
            print("   ✓ Home page loads successfully")
        else:
            print(f"   ✗ Home page failed with status {response.status_code}")
    except Exception as e:
        print(f"   ✗ Home page error: {e}")
    
    # Test login page
    print("2. Testing login page...")
    try:
        response = client.get('/accounts/login/')
        if response.status_code == 200:
            print("   ✓ Login page loads successfully")
        else:
            print(f"   ✗ Login page failed with status {response.status_code}")
    except Exception as e:
        print(f"   ✗ Login page error: {e}")
    
    # Test register page
    print("3. Testing register page...")
    try:
        response = client.get('/accounts/register/')
        if response.status_code == 200:
            print("   ✓ Register page loads successfully")
        else:
            print(f"   ✗ Register page failed with status {response.status_code}")
    except Exception as e:
        print(f"   ✗ Register page error: {e}")
    
    # Create test user
    print("4. Creating test user...")
    try:
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        print("   ✓ Test user created successfully")
        
        # Login with test user
        login_success = client.login(username='testuser', password='testpass123')
        if login_success:
            print("   ✓ User login successful")
        else:
            print("   ✗ User login failed")
            
        # Test dashboard access
        print("5. Testing dashboard access...")
        response = client.get('/dashboard/')
        if response.status_code == 200:
            print("   ✓ Dashboard loads successfully")
        else:
            print(f"   ✗ Dashboard failed with status {response.status_code}")
            
        # Test projects page
        print("6. Testing projects page...")
        response = client.get('/projects/')
        if response.status_code == 200:
            print("   ✓ Projects page loads successfully")
        else:
            print(f"   ✗ Projects page failed with status {response.status_code}")
            
        # Test bugs page
        print("7. Testing bugs page...")
        response = client.get('/bugs/')
        if response.status_code == 200:
            print("   ✓ Bugs page loads successfully")
        else:
            print(f"   ✗ Bugs page failed with status {response.status_code}")
            
        # Test recent activity page
        print("8. Testing recent activity page...")
        response = client.get('/dashboard/recent-activity/')
        if response.status_code == 200:
            print("   ✓ Recent activity page loads successfully")
        else:
            print(f"   ✗ Recent activity page failed with status {response.status_code}")
            
    except Exception as e:
        print(f"   ✗ User creation/testing error: {e}")
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == '__main__':
    test_basic_functionality()
