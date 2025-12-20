#!/usr/bin/env python3
"""
Script untuk test real-time notification system
Membuat beberapa notifications dengan timestamp yang berbeda untuk testing
"""

import sqlite3
import os
from datetime import datetime, timedelta
import random

def create_test_notifications():
    """Buat test notifications untuk testing real-time formatting"""
    
    # Connect to database
    db_path = 'instance/database.db'
    if not os.path.exists(db_path):
        print("Database tidak ditemukan! Jalankan aplikasi terlebih dahulu.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get current user (assuming user ID 1 exists)
    cursor.execute("SELECT id FROM user LIMIT 1")
    user_result = cursor.fetchone()
    
    if not user_result:
        print("Tidak ada user ditemukan! Buat user admin terlebih dahulu.")
        return
    
    user_id = user_result[0]
    
    # Get some job IDs for notifications
    cursor.execute("SELECT id FROM job_application LIMIT 3")
    jobs = cursor.fetchall()
    
    # Clear existing notifications for testing
    cursor.execute("DELETE FROM notification WHERE user_id = ?", (user_id,))
    
    # Create test notifications with different timestamps
    test_notifications = [
        # Very recent notification (10 seconds ago)
        {
            'title': '🔔 Test - Baru Saja',
            'message': 'Notifikasi test yang dibuat 10 detik yang lalu untuk testing real-time formatting',
            'type': 'info',
            'timestamp': datetime.now() - timedelta(seconds=10)
        },
        # Recent notification (2 minutes ago)
        {
            'title': '📧 Test - 2 Menit Lalu',
            'message': 'Notifikasi test yang dibuat 2 menit yang lalu untuk testing menit formatting',
            'type': 'info',
            'timestamp': datetime.now() - timedelta(minutes=2)
        },
        # Recent notification (1 hour ago)
        {
            'title': '⚡ Test - 1 Jam Lalu',
            'message': 'Notifikasi test yang dibuat 1 jam yang lalu untuk testing jam formatting',
            'type': 'info',
            'timestamp': datetime.now() - timedelta(hours=1)
        },
        # Recent notification (1 day ago)
        {
            'title': '📅 Test - 1 Hari Lalu',
            'message': 'Notifikasi test yang dibuat 1 hari yang lalu untuk testing hari formatting',
            'type': 'info',
            'timestamp': datetime.now() - timedelta(days=1)
        },
        # Success notification
        {
            'title': '🎉 Test - Success',
            'message': 'Notifikasi success test untuk testing success type',
            'type': 'success',
            'timestamp': datetime.now() - timedelta(minutes=30)
        },
        # Warning notification
        {
            'title': '⚠️ Test - Warning',
            'message': 'Notifikasi warning test untuk testing warning type',
            'type': 'warning',
            'timestamp': datetime.now() - timedelta(hours=2)
        }
    ]
    
    print(f"Creating {len(test_notifications)} test notifications...")
    
    for i, notif in enumerate(test_notifications):
        job_id = jobs[i % len(jobs)][0] if jobs else None
        
        cursor.execute("""
            INSERT INTO notification (user_id, title, message, type, is_read, job_id, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            notif['title'],
            notif['message'],
            notif['type'],
            random.choice([True, False]),  # Random read status
            job_id,
            notif['timestamp']
        ))
        
        print(f"✓ Created: {notif['title']} - {notif['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Test notifications created successfully!")
    print(f"📊 Total notifications: {len(test_notifications)}")
    print(f"🕒 Created at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n📱 Test these scenarios:")
    print(f"   • Open browser console (F12) to see debugging logs")
    print(f"   • Click notification bell to see notifications")
    print(f"   • Watch the timestamps change in real-time")
    print(f"   • Should show: 'Baru saja', '2 menit yang lalu', '1 jam yang lalu', etc.")

def show_notifications():
    """Show current notifications in database"""
    db_path = 'instance/database.db'
    if not os.path.exists(db_path):
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, title, message, type, is_read, created_at 
        FROM notification 
        ORDER BY created_at DESC 
        LIMIT 10
    """)
    
    notifications = cursor.fetchall()
    
    print("\n📋 Current Notifications:")
    print("-" * 80)
    
    for notif in notifications:
        print(f"ID: {notif[0]}")
        print(f"Title: {notif[1]}")
        print(f"Type: {notif[3]} | Read: {'Yes' if notif[4] else 'No'}")
        print(f"Created: {notif[5]}")
        print(f"Message: {notif[2][:60]}...")
        print("-" * 40)
    
    conn.close()

if __name__ == "__main__":
    print("🚀 Testing Real-Time Notification System")
    print("=" * 50)
    
    # Create test notifications
    create_test_notifications()
    
    # Show current notifications
    show_notifications()
    
    print(f"\n💡 Instructions:")
    print(f"1. Open your browser at http://localhost:5001")
    print(f"2. Login dengan admin/admin")
    print(f"3. Open browser console (F12)")
    print(f"4. Click the notification bell icon")
    print(f"5. Watch the timestamps update in real-time!")
    print(f"6. Check console for debugging logs")

