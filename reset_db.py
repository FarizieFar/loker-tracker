#!/usr/bin/env python3
"""
Script untuk reset database dengan struktur model yang benar
"""

import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User, Status, JobApplication

def reset_database():
    """Reset dan buat ulang database dengan struktur yang benar"""
    
    with app.app_context():
        try:
            # Drop all tables
            print("🗑️  Menghapus tabel lama...")
            db.drop_all()
            
            # Create all tables with new structure
            print("🔧 Membuat tabel baru...")
            db.create_all()
            
            # Seed status data
            print("📊 Menambahkan data status...")
            statuses = [
                Status(name='Terdaftar', color='secondary'),
                Status(name='Interview', color='info'),
                Status(name='Tes', color='warning'),
                Status(name='Diterima', color='success'),
                Status(name='Tidak Diterima', color='danger')
            ]
            
            for status in statuses:
                db.session.add(status)
            
            db.session.commit()
            
            print("✅ Database berhasil di-reset!")
            print("📋 Struktur tabel baru:")
            print("   - JobApplication dengan field: position, application_proof, image_proof, source_info, logo_url, notes")
            print("   - Status dengan 5 kategori")
            print("   - User dengan authentication")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            db.session.rollback()

if __name__ == '__main__':
    reset_database()
