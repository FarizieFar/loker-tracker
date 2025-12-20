
#!/usr/bin/env python3
"""
Debug script untuk mengecek format timestamp dan waktu
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the app and db directly from app.py
from app import app, db
from models import JobApplication

def debug_timestamps():
    """Debug timestamp formats"""
    with app.app_context():
        print("=== DEBUG TIMESTAMP ISSUE ===")
        
        # Check some job applications
        jobs = JobApplication.query.limit(5).all()
        
        for job in jobs:
            print(f"\n--- Job ID: {job.id} ---")
            print(f"Position: {job.position}")
            print(f"Applied date: {job.applied_date}")
            print(f"Last status update: {job.last_status_update}")
            print(f"Applied date type: {type(job.applied_date)}")
            print(f"Last status update type: {type(job.last_status_update)}")
            
            if job.applied_date:
                print(f"Applied ISO format: {job.applied_date.isoformat()}")
            if job.last_status_update:
                print(f"Last status ISO format: {job.last_status_update.isoformat()}")
                print(f"Last status timezone: {job.last_status_update.tzinfo}")
            
            # Check current server time
            from datetime import datetime
            now = datetime.now()
            print(f"Server current time: {now}")
            print(f"Server time ISO: {now.isoformat()}")
            
            if job.last_status_update:
                diff = now - job.last_status_update
                print(f"Time difference: {diff}")
                print(f"Diff in seconds: {diff.total_seconds()}")
                print(f"Diff in hours: {diff.total_seconds() / 3600}")
            
            print("-" * 50)

if __name__ == "__main__":
    debug_timestamps()
