#!/usr/bin/env python3
"""
Script untuk memperbaiki timestamp issue - update last_status_update untuk semua job
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the app and db directly from app.py
from app import app, db
from models import JobApplication
from datetime import datetime

def fix_timestamps():
    """Update semua last_status_update ke waktu saat ini untuk testing"""
    with app.app_context():
        print("=== FIXING TIMESTAMP ISSUE ===")
        
        # Get all jobs
        jobs = JobApplication.query.all()
        
        print(f"Total jobs found: {len(jobs)}")
        
        now = datetime.now()
        print(f"Setting all last_status_update to: {now}")
        
        # Update all jobs
        for job in jobs:
            print(f"Updating Job ID: {job.id} - {job.position}")
            job.last_status_update = now
        
        # Commit changes
        db.session.commit()
        
        print("All timestamps updated successfully!")
        
        # Verify one job
        if jobs:
            test_job = jobs[0]
            print(f"\nVerification - Job ID: {test_job.id}")
            print(f"Position: {test_job.position}")
            print(f"Last status update: {test_job.last_status_update}")
            
            diff = now - test_job.last_status_update
            print(f"Time difference: {diff}")
            print(f"Should show: Baru saja")

if __name__ == "__main__":
    fix_timestamps()
