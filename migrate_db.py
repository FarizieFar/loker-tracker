#!/usr/bin/env python3
"""
Database Migration Script for Loker Tracker
Adds new fields: position, application_proof, image_proof
"""

import sqlite3
import os
from datetime import datetime

def migrate_database():
    """Migrate database to add new fields"""
    
    # Database path
    db_path = 'instance/database.db'
    
    if not os.path.exists(db_path):
        print(f"Database file not found: {db_path}")
        print("Please run the application first to create the database.")
        return
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔄 Starting database migration...")
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(job_application)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add position column if not exists
        if 'position' not in columns:
            cursor.execute("ALTER TABLE job_application ADD COLUMN position VARCHAR(100)")
            print("✅ Added 'position' column")
        else:
            print("ℹ️ 'position' column already exists")
        
        # Add application_proof column if not exists
        if 'application_proof' not in columns:
            cursor.execute("ALTER TABLE job_application ADD COLUMN application_proof TEXT")
            print("✅ Added 'application_proof' column")
        else:
            print("ℹ️ 'application_proof' column already exists")
            

        # Add image_proof column if not exists
        if 'image_proof' not in columns:
            cursor.execute("ALTER TABLE job_application ADD COLUMN image_proof VARCHAR(255)")
            print("✅ Added 'image_proof' column")
        else:
            print("ℹ️ 'image_proof' column already exists")
            
        # Add source_info column if not exists
        if 'source_info' not in columns:
            cursor.execute("ALTER TABLE job_application ADD COLUMN source_info VARCHAR(100)")
            print("✅ Added 'source_info' column")
        else:
            print("ℹ️ 'source_info' column already exists")
        
        # Commit changes
        conn.commit()
        
        # Show updated table structure
        cursor.execute("PRAGMA table_info(job_application)")
        updated_columns = cursor.fetchall()
        
        print("\n📊 Updated table structure:")
        for col in updated_columns:
            print(f"  - {col[1]} ({col[2]})")
        
        print("\n🎉 Database migration completed successfully!")
        
        # Show sample data if exists
        cursor.execute("SELECT COUNT(*) FROM job_application")
        count = cursor.fetchone()[0]
        print(f"\n📈 Total job applications: {count}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    migrate_database()
