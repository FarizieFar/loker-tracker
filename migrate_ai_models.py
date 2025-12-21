
#!/usr/bin/env python3
"""
Database Migration: Add AI Models
Creates tables for AI-powered features in the job tracker
"""

import sqlite3
import os
from datetime import datetime

def migrate_ai_models():
    """Create AI-related database tables"""
    
    # Path to database
    db_path = 'instance/database.db'
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return False
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if AI tables already exist
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='cv_profile'
        """)
        
        if cursor.fetchone():
            print("AI tables already exist, skipping migration")
            conn.close()
            return True
        
        print("🚀 Starting AI Models Migration...")
        
        # Create CVProfile table
        print("📊 Creating CVProfile table...")
        cursor.execute("""
            CREATE TABLE cv_profile (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                full_name VARCHAR(100),
                email VARCHAR(100),
                phone VARCHAR(20),
                location VARCHAR(100),
                extracted_skills TEXT,
                experience_level VARCHAR(20),
                years_experience INTEGER,
                education_level VARCHAR(50),
                summary TEXT,
                cv_file_path VARCHAR(255),
                file_size INTEGER,
                ats_score FLOAT,
                completeness_score FLOAT,
                last_updated DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user (id)
            )
        """)
        
        # Create JobMatch table
        print("📊 Creating JobMatch table...")
        cursor.execute("""
            CREATE TABLE job_match (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                job_id INTEGER NOT NULL,
                match_score FLOAT,
                matching_skills TEXT,
                missing_skills TEXT,
                additional_skills TEXT,
                compatibility_factors TEXT,
                recommendations TEXT,
                salary_match_score FLOAT,
                location_match_score FLOAT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user (id),
                FOREIGN KEY (job_id) REFERENCES job_application (id)
            )
        """)
        
        # Create AIInsight table
        print("📊 Creating AIInsight table...")
        cursor.execute("""
            CREATE TABLE ai_insight (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                insight_type VARCHAR(50),
                title VARCHAR(200) NOT NULL,
                content TEXT NOT NULL,
                confidence_score FLOAT,
                priority_level INTEGER DEFAULT 3,
                is_read BOOLEAN DEFAULT 0,
                is_dismissed BOOLEAN DEFAULT 0,
                action_required BOOLEAN DEFAULT 0,
                action_text VARCHAR(500),
                related_skills TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                expires_at DATETIME,
                FOREIGN KEY (user_id) REFERENCES user (id)
            )
        """)
        
        # Create SkillGap table
        print("📊 Creating SkillGap table...")
        cursor.execute("""
            CREATE TABLE skill_gap (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                skill_name VARCHAR(100) NOT NULL,
                skill_category VARCHAR(50),
                current_level VARCHAR(20),
                required_level VARCHAR(20),
                gap_severity FLOAT,
                learning_resources TEXT,
                estimated_time_to_learn INTEGER,
                priority_score FLOAT,
                demand_score FLOAT,
                salary_impact FLOAT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user (id)
            )
        """)
        
        # Create CareerTrajectory table
        print("📊 Creating CareerTrajectory table...")
        cursor.execute("""
            CREATE TABLE career_trajectory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                current_role VARCHAR(100),
                target_role VARCHAR(100),
                career_stage VARCHAR(50),
                trajectory_score FLOAT,
                progression_years FLOAT,
                success_probability FLOAT,
                recommended_actions TEXT,
                skill_development_plan TEXT,
                industry_transition_score FLOAT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user (id)
            )
        """)
        
        # Create indexes for better performance
        print("📊 Creating indexes...")
        indexes = [
            "CREATE INDEX idx_cv_profile_user_id ON cv_profile(user_id)",
            "CREATE INDEX idx_job_match_user_id ON job_match(user_id)",
            "CREATE INDEX idx_job_match_job_id ON job_match(job_id)",
            "CREATE INDEX idx_ai_insight_user_id ON ai_insight(user_id)",
            "CREATE INDEX idx_ai_insight_is_read ON ai_insight(is_read)",
            "CREATE INDEX idx_skill_gap_user_id ON skill_gap(user_id)",
            "CREATE INDEX idx_career_trajectory_user_id ON career_trajectory(user_id)"
        ]
        
        for index_sql in indexes:
            cursor.execute(index_sql)
        
        # Commit changes
        conn.commit()
        
        print("✅ Migration completed successfully!")
        print("\n📋 Created AI Tables:")
        print("   • cv_profile - CV/Resume analysis and extracted information")
        print("   • job_match - Job matching results between CV and job applications") 
        print("   • ai_insight - AI-generated insights and recommendations")
        print("   • skill_gap - Identified skill gaps and recommendations")
        print("   • career_trajectory - Career path analysis and predictions")
        print(f"\n📊 Created {len(indexes)} indexes for better performance")
        
        # Verify tables were created
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name IN ('cv_profile', 'job_match', 'ai_insight', 'skill_gap', 'career_trajectory')
        """)
        
        created_tables = [row[0] for row in cursor.fetchall()]
        
        print(f"\n🎯 Verified {len(created_tables)}/5 AI tables created:")
        for table in created_tables:
            print(f"   ✅ {table}")
            
        missing_tables = ['cv_profile', 'job_match', 'ai_insight', 'skill_gap', 'career_trajectory']
        missing_tables = [table for table in missing_tables if table not in created_tables]
        if missing_tables:
            print(f"\n❌ Missing tables: {missing_tables}")
            
        print("\n🎉 AI Database Migration Complete!")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        if 'conn' in locals():
            conn.close()
        return False

if __name__ == "__main__":
    print("🚀 Memulai migrasi database untuk fitur AI...")
    
    if not migrate_ai_models():
        print("❌ Migrasi database gagal!")
        exit(1)
    
    print("\n🎉 Migrasi database AI selesai!")
    print("Database siap untuk fitur AI-powered!")
