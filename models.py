



from flask_login import UserMixin
from extensions import db
from datetime import datetime as dt

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    jobs = db.relationship(
        'JobApplication',
        backref='user',
        lazy=True
    )
    
    notifications = db.relationship(
        'Notification',
        backref='user',
        lazy=True
    )

class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    color = db.Column(db.String(20), default='secondary')

    jobs = db.relationship(
        'JobApplication',
        backref='status',
        lazy=True
    )


class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100))
    position = db.Column(db.String(100), nullable=True)  # NEW: Posisi yang dilamar
    location = db.Column(db.String(100))
    address = db.Column(db.String(200))

    application_proof = db.Column(db.Text, nullable=True)  # NEW: Link atau path screenshot
    image_proof = db.Column(db.String(255), nullable=True)  # NEW: Path to uploaded image
    source_info = db.Column(db.String(100), nullable=True)  # NEW: Asal info loker
    logo_url = db.Column(db.String(255), nullable=True)  # NEW: URL logo perusahaan
    notes = db.Column(db.Text, nullable=True)  # NEW: Keterangan tambahan
    applied_date = db.Column(db.DateTime)
    last_status_update = db.Column(db.DateTime, nullable=True)  # NEW: Tanggal terakhir update status

    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(20), default='info')  # info, success, warning, danger
    is_read = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=dt.utcnow)
    
    # Link to related job if applicable
    job_id = db.Column(db.Integer, db.ForeignKey('job_application.id'), nullable=True)


# AI-Powered Models
class CVProfile(db.Model):
    """User's CV/Resume analysis and extracted information"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Extracted CV data
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    location = db.Column(db.String(100))
    
    # Skills and experience
    extracted_skills = db.Column(db.Text)  # JSON array of skills
    experience_level = db.Column(db.String(20))  # junior, mid, senior, expert
    years_experience = db.Column(db.Integer)
    education_level = db.Column(db.String(50))
    
    # CV content analysis
    summary = db.Column(db.Text)
    cv_file_path = db.Column(db.String(255))
    file_size = db.Column(db.Integer)
    
    # Analysis metadata
    ats_score = db.Column(db.Float)  # ATS compatibility score (0-100)
    completeness_score = db.Column(db.Float)  # CV completeness (0-100)
    last_updated = db.Column(db.DateTime, default=dt.utcnow, onupdate=dt.utcnow)
    
    created_at = db.Column(db.DateTime, default=dt.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='cv_profiles')


class JobMatch(db.Model):
    """Job matching results between CV and job applications"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job_application.id'), nullable=False)
    
    # Matching results
    match_score = db.Column(db.Float)  # 0-100 percentage
    matching_skills = db.Column(db.Text)  # JSON array of matching skills
    missing_skills = db.Column(db.Text)  # JSON array of missing skills
    additional_skills = db.Column(db.Text)  # JSON array of extra skills
    
    # Analysis results
    compatibility_factors = db.Column(db.Text)  # JSON object with factors
    recommendations = db.Column(db.Text)  # Text recommendations
    salary_match_score = db.Column(db.Float)  # 0-100
    location_match_score = db.Column(db.Float)  # 0-100
    
    created_at = db.Column(db.DateTime, default=dt.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='job_matches')
    job = db.relationship('JobApplication', backref='job_matches')


class AIInsight(db.Model):
    """AI-generated insights and recommendations for users"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Insight details
    insight_type = db.Column(db.String(50))  # career_path, skill_gap, market_trend, success_prediction
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    # Analysis metadata
    confidence_score = db.Column(db.Float)  # 0-1 confidence in the insight
    priority_level = db.Column(db.Integer, default=3)  # 1-5 priority level
    is_read = db.Column(db.Boolean, default=False)
    is_dismissed = db.Column(db.Boolean, default=False)
    
    # Actionable data
    action_required = db.Column(db.Boolean, default=False)
    action_text = db.Column(db.String(500))
    related_skills = db.Column(db.Text)  # JSON array of relevant skills
    
    created_at = db.Column(db.DateTime, default=dt.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    user = db.relationship('User', backref='ai_insights')


class SkillGap(db.Model):
    """Identified skill gaps and recommendations"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Skill information
    skill_name = db.Column(db.String(100), nullable=False)
    skill_category = db.Column(db.String(50))  # technical, soft, language, etc.
    
    # Gap analysis
    current_level = db.Column(db.String(20))  # none, basic, intermediate, advanced, expert
    required_level = db.Column(db.String(20))
    gap_severity = db.Column(db.Float)  # 0-1 severity score
    
    # Recommendations
    learning_resources = db.Column(db.Text)  # JSON array of learning resources
    estimated_time_to_learn = db.Column(db.Integer)  # hours
    priority_score = db.Column(db.Float)  # 0-1 priority for learning
    
    # Market data
    demand_score = db.Column(db.Float)  # 0-1 market demand
    salary_impact = db.Column(db.Float)  # 0-1 potential salary increase
    
    created_at = db.Column(db.DateTime, default=dt.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='skill_gaps')


class CareerTrajectory(db.Model):
    """User's career path analysis and predictions"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Career data
    current_role = db.Column(db.String(100))
    target_role = db.Column(db.String(100))
    career_stage = db.Column(db.String(50))  # entry, early, mid, senior, executive
    
    # Analysis results
    trajectory_score = db.Column(db.Float)  # 0-100 current trajectory strength
    progression_years = db.Column(db.Float)  # estimated years to next level
    success_probability = db.Column(db.Float)  # 0-1 probability of reaching target
    
    # Recommendations
    recommended_actions = db.Column(db.Text)  # JSON array of actions
    skill_development_plan = db.Column(db.Text)  # JSON object with timeline
    industry_transition_score = db.Column(db.Float)  # 0-100 for industry changes
    
    created_at = db.Column(db.DateTime, default=dt.utcnow)
    last_updated = db.Column(db.DateTime, default=dt.utcnow, onupdate=dt.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='career_trajectories')





