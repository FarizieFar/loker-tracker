#!/usr/bin/env python3
"""
Script untuk memperbaiki timestamp notifikasi issue
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the app and db directly from app.py
from app import app, db
from models import Notification
from datetime import datetime, timedelta

def fix_notification_timestamps():
    """Update notifikasi yang timestamp-nya lama ke waktu yang lebih baru untuk testing"""
    with app.app_context():
        print("=== FIXING NOTIFICATION TIMESTAMP ISSUE ===")
        
        # Get all notifications
        notifications = Notification.query.all()
        
        print(f"Total notifications found: {len(notifications)}")
        
        # Current time
        now = datetime.now()
        print(f"Current time: {now}")
        
        # Create different timestamps for testing
        timestamps = [
            now,  # Baru saja
            now - timedelta(minutes=5),  # 5 menit yang lalu
            now - timedelta(minutes=30),  # 30 menit yang lalu
            now - timedelta(hours=2),  # 2 jam yang lalu
            now - timedelta(hours=7),  # 7 jam yang lalu (seperti yang bermasalah)
            now - timedelta(days=1),  # 1 hari yang lalu
        ]
        
        print("Updating notification timestamps...")
        
        for i, notification in enumerate(notifications):
            if i < len(timestamps):
                new_timestamp = timestamps[i]
                print(f"Updating Notification ID: {notification.id}")
                print(f"  Title: {notification.title}")
                print(f"  Old created_at: {notification.created_at}")
                print(f"  New created_at: {new_timestamp}")
                notification.created_at = new_timestamp
        
        # Commit changes
        db.session.commit()
        
        print("\nAll notification timestamps updated successfully!")
        
        # Verify some notifications
        if notifications:
            print(f"\n=== VERIFICATION ===")
            for i, notification in enumerate(notifications[:5]):
                if i < len(timestamps):
                    diff = now - notification.created_at
                    hours = diff.total_seconds() / 3600
                    
                    if hours < 1:
                        if hours * 60 < 1:
                            display = "Baru saja"
                        else:
                            display = f"{int(hours * 60)} menit yang lalu"
                    else:
                        display = f"{int(hours)} jam yang lalu"
                    
                    print(f"Notification {notification.id}: {display}")
                    print(f"  Title: {notification.title}")
                    print(f"  Timestamp: {notification.created_at}")
                    print("-" * 50)

if __name__ == "__main__":
    fix_notification_timestamps()
