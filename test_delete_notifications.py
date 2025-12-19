#!/usr/bin/env python3
"""
Script untuk test endpoint delete notifications
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:5001"
LOGIN_URL = f"{BASE_URL}/login"
API_NOTIFICATIONS_URL = f"{BASE_URL}/api/notifications"

def login_and_get_cookies():
    """Login dan return session cookies"""
    session = requests.Session()
    
    # Get login page untuk CSRF token (jika ada)
    login_page = session.get(LOGIN_URL)
    
    # Login data
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    # Login
    response = session.post(LOGIN_URL, data=login_data)
    
    if response.status_code == 200:
        print("✅ Login berhasil")
        return session
    else:
        print(f"❌ Login gagal: {response.status_code}")
        return None

def test_delete_notification():
    """Test delete individual notification"""
    session = login_and_get_cookies()
    if not session:
        return
    
    # Get notifications terlebih dahulu
    response = session.get(API_NOTIFICATIONS_URL)
    if response.status_code != 200:
        print(f"❌ Gagal get notifications: {response.status_code}")
        return
    
    data = response.json()
    if not data.get('notifications'):
        print("ℹ️ Tidak ada notifications untuk di-delete")
        return
    
    # Get first notification untuk di-delete
    first_notification = data['notifications'][0]
    notification_id = first_notification['id']
    
    print(f"🗑️ Delete notification ID: {notification_id}")
    print(f"   Title: {first_notification['title']}")
    
    # Test delete
    delete_url = f"{BASE_URL}/api/notifications/{notification_id}"
    response = session.delete(delete_url)
    
    if response.status_code == 200:
        print("✅ Notification berhasil di-delete")
        print(f"   Response: {response.json()}")
    else:
        print(f"❌ Gagal delete notification: {response.status_code}")
        print(f"   Response: {response.text}")

def test_clear_all_notifications():
    """Test clear all notifications"""
    session = login_and_get_cookies()
    if not session:
        return
    
    # Get notifications terlebih dahulu
    response = session.get(API_NOTIFICATIONS_URL)
    if response.status_code != 200:
        print(f"❌ Gagal get notifications: {response.status_code}")
        return
    
    data = response.json()
    if not data.get('notifications'):
        print("ℹ️ Tidak ada notifications untuk di-clear")
        return
    
    notification_count = len(data['notifications'])
    print(f"🗑️ Clear all notifications ({notification_count} items)")
    
    # Test clear all
    clear_url = f"{BASE_URL}/api/notifications/clear_all"
    response = session.delete(clear_url)
    
    if response.status_code == 200:
        print("✅ Semua notifications berhasil di-clear")
        print(f"   Response: {response.json()}")
    else:
        print(f"❌ Gagal clear notifications: {response.status_code}")
        print(f"   Response: {response.text}")

if __name__ == "__main__":
    print("🧪 Testing Delete Notifications API")
    print("=" * 50)
    
    print("\n1. Testing Delete Individual Notification:")
    test_delete_notification()
    
    print("\n2. Testing Clear All Notifications:")
    test_clear_all_notifications()
    
    print("\n" + "=" * 50)
    print("✅ Testing selesai")
