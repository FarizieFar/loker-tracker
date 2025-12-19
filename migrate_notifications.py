#!/usr/bin/env python3
"""
Script migrasi untuk menambahkan tabel Notification ke database yang sudah ada
"""

import sqlite3
import os
from datetime import datetime

def migrate_notifications():
    """Menambahkan tabel Notification ke database yang sudah ada"""
    
    # Path ke database
    db_path = 'instance/database.db'
    
    if not os.path.exists(db_path):
        print(f"Database tidak ditemukan di {db_path}")
        return False
    
    try:
        # Connect ke database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Cek apakah tabel notifications sudah ada
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='notification'
        """)
        
        if cursor.fetchone():
            print("Tabel 'notification' sudah ada, skip migrasi")
            conn.close()
            return True
        
        # Buat tabel notification
        cursor.execute("""
            CREATE TABLE notification (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title VARCHAR(100) NOT NULL,
                message TEXT NOT NULL,
                type VARCHAR(20) DEFAULT 'info',
                is_read BOOLEAN DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                job_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES user (id),
                FOREIGN KEY (job_id) REFERENCES job_application (id)
            )
        """)
        
        # Tambahkan foreign key constraint untuk user_id
        cursor.execute("""
            CREATE INDEX idx_notification_user_id ON notification(user_id)
        """)
        
        # Tambahkan foreign key constraint untuk job_id
        cursor.execute("""
            CREATE INDEX idx_notification_job_id ON notification(job_id)
        """)
        
        # Commit perubahan
        conn.commit()
        
        print("✅ Migrasi tabel notification berhasil!")
        print("Tabel 'notification' telah dibuat dengan kolom:")
        print("  - id (PRIMARY KEY)")
        print("  - user_id (FOREIGN KEY)")
        print("  - title (VARCHAR 100)")
        print("  - message (TEXT)")
        print("  - type (VARCHAR 20, default 'info')")
        print("  - is_read (BOOLEAN, default 0)")
        print("  - created_at (DATETIME, default CURRENT_TIMESTAMP)")
        print("  - job_id (FOREIGN KEY, nullable)")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error saat migrasi: {str(e)}")
        if 'conn' in locals():
            conn.close()
        return False

def add_notifications_for_existing_jobs():
    """Menambahkan notifikasi untuk job yang sudah ada berdasarkan status"""
    
    db_path = 'instance/database.db'
    
    if not os.path.exists(db_path):
        print(f"Database tidak ditemukan di {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Ambil semua job yang ada
        cursor.execute("""
            SELECT ja.id, ja.company_name, ja.position, s.name as status_name, ja.user_id
            FROM job_application ja
            JOIN status s ON ja.status_id = s.id
        """)
        
        jobs = cursor.fetchall()
        
        if not jobs:
            print("Tidak ada job untuk dibuatkan notifikasi")
            conn.close()
            return True
        
        # Buat notifikasi untuk setiap job berdasarkan status
        notifications_created = 0
        
        for job_id, company_name, position, status_name, user_id in jobs:
            # Skip jika status adalah "Terdaftar" (default status)
            if status_name == "Terdaftar":
                continue
            
            # Tentukan tipe dan pesan notifikasi berdasarkan status
            notification_type = "info"
            notification_title = "Status Lamaran Diupdate"
            notification_message = f"Status lamaran di {company_name} berhasil diubah menjadi {status_name}"
            
            if status_name == "Diterima":
                notification_type = "success"
                notification_title = "🎉 Selamat! Lamaran Diterima!"
                notification_message = f"Selamat! Lamaran Anda di {company_name} untuk posisi {position or 'Posisi'} telah diterima!"
            elif status_name == "Tidak Diterima":
                notification_type = "warning"
                notification_title = "Lamaran Tidak Diterima"
                notification_message = f"Maaf, lamaran Anda di {company_name} untuk posisi {position or 'Posisi'} tidak diterima. Jangan menyerah!"
            elif status_name == "Interview":
                notification_type = "info"
                notification_title = "📞 Undangan Interview"
                notification_message = f"Anda mendapat undangan interview untuk posisi {position or 'Posisi'} di {company_name}. Persiapkan diri dengan baik!"
            elif status_name == "Tes":
                notification_type = "info"
                notification_title = "📝 Undangan Tes"
                notification_message = f"Anda mendapat undangan tes untuk posisi {position or 'Posisi'} di {company_name}. Belajar dan persiapan yang matang!"
            
            # Insert notifikasi
            cursor.execute("""
                INSERT INTO notification (user_id, title, message, type, job_id, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, notification_title, notification_message, notification_type, job_id, datetime.utcnow()))
            
            notifications_created += 1
        
        # Commit perubahan
        conn.commit()
        
        print(f"✅ Berhasil membuat {notifications_created} notifikasi untuk job yang sudah ada")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error saat membuat notifikasi: {str(e)}")
        if 'conn' in locals():
            conn.close()
        return False

if __name__ == "__main__":
    print("🚀 Memulai migrasi sistem notifikasi...")
    
    # Step 1: Buat tabel notification
    print("\n📋 Step 1: Membuat tabel notification...")
    if not migrate_notifications():
        print("❌ Migrasi tabel gagal!")
        exit(1)
    
    # Step 2: Buat notifikasi untuk job yang sudah ada
    print("\n📋 Step 2: Membuat notifikasi untuk job yang sudah ada...")
    if not add_notifications_for_existing_jobs():
        print("❌ Pembuatan notifikasi gagal!")
        exit(1)
    
    print("\n🎉 Migrasi sistem notifikasi selesai!")
    print("Sistem notifikasi siap digunakan!")

