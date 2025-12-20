#!/usr/bin/env python3
"""
Migration script untuk menambahkan field last_status_update ke JobApplication
Script ini akan:
1. Menambahkan field last_status_update ke tabel yang sudah ada
2. Mengisi field tersebut dengan nilai applied_date untuk data existing (asumsi status terakhir diubah saat apply)
"""

import sqlite3
import os
from datetime import datetime

def migrate_database():
    """Migrate database untuk menambahkan field last_status_update"""
    
    db_path = 'instance/database.db'
    
    if not os.path.exists(db_path):
        print(f"Database tidak ditemukan di: {db_path}")
        return False
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🗄️  Menghubungkan ke database...")
        
        # Check if column already exists
        cursor.execute("PRAGMA table_info(job_application)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'last_status_update' in columns:
            print("✅ Field last_status_update sudah ada di database")
            return True
        
        print("📝 Menambahkan field last_status_update ke tabel job_application...")
        
        # Add the column (initially NULL)
        cursor.execute("""
            ALTER TABLE job_application 
            ADD COLUMN last_status_update DATETIME
        """)
        
        print("🔄 Mengupdate data existing...")
        
        # For existing records, set last_status_update = applied_date (assuming status was last updated when applied)
        # Only update records that don't have a last_status_update value
        cursor.execute("""
            UPDATE job_application 
            SET last_status_update = applied_date 
            WHERE last_status_update IS NULL
        """)
        
        # Get count of updated records
        updated_count = cursor.rowcount
        print(f"✅ Berhasil mengupdate {updated_count} records")
        
        # Commit changes
        conn.commit()
        
        print("🎉 Migration berhasil diselesaikan!")
        print(f"   - Field last_status_update berhasil ditambahkan")
        print(f"   - {updated_count} existing records telah diupdate")
        
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Error saat migrasi database: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Error tidak terduga: {e}")
        return False
        
    finally:
        if conn:
            conn.close()

def verify_migration():
    """Verify bahwa migration berhasil"""
    
    db_path = 'instance/database.db'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check column exists
        cursor.execute("PRAGMA table_info(job_application)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'last_status_update' in columns:
            print("✅ Field last_status_update berhasil ditambahkan")
        else:
            print("❌ Field last_status_update tidak ditemukan")
            return False
        
        # Check some sample data
        cursor.execute("""
            SELECT id, company_name, applied_date, last_status_update 
            FROM job_application 
            LIMIT 5
        """)
        
        sample_data = cursor.fetchall()
        
        if sample_data:
            print("📊 Sample data:")
            for row in sample_data:
                print(f"   ID: {row[0]}, Company: {row[1]}, Applied: {row[2]}, Last Update: {row[3]}")
        else:
            print("ℹ️  Tidak ada data job application yang ditemukan")
        
        return True
        
    except Exception as e:
        print(f"❌ Error saat verifikasi: {e}")
        return False
        
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("🚀 Starting Migration: Menambahkan Field last_status_update")
    print("=" * 60)
    
    # Run migration
    success = migrate_database()
    
    if success:
        print("\n🔍 Verifying migration...")
        verify_migration()
        print("\n✅ Migration completed successfully!")
    else:
        print("\n❌ Migration failed!")
    
    print("=" * 60)
