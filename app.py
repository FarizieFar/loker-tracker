



from flask import Flask, render_template, redirect, url_for, request, flash, abort, jsonify, send_file, Response
from datetime import datetime, date
from extensions import db

from models import JobApplication, User, Status, Notification
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
import os
import uuid
import io
from io import BytesIO


# Import for PDF and Excel export
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch

# Import AI modules
from ai_modules.ai_service import AIService
from ai_modules.cv_analyzer import CVAnalyzer
from ai_modules.job_matcher import JobMatcher
from ai_modules.insights_generator import InsightsGenerator
from models import CVProfile, JobMatch, AIInsight, SkillGap, CareerTrajectory
import json
import traceback


app = Flask(__name__)


app.config['SECRET_KEY'] = 'super-secret-key-alfarizi'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# File upload configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads/proofs'
app.config['CV_UPLOAD_FOLDER'] = 'static/uploads/cv'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
CV_ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}

# Create upload directories if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['CV_UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Check if file has allowed extension for images"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_cv_file(filename):
    """Check if file has allowed extension for CV uploads"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in CV_ALLOWED_EXTENSIONS

def save_uploaded_file(file):
    """Save uploaded file and return filename"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add unique identifier to prevent conflicts
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        return unique_filename
    return None

def save_uploaded_image(file):
    """Save uploaded image and return the filename"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Generate unique filename
        unique_filename = str(uuid.uuid4()) + '.' + filename.rsplit('.', 1)[1]
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        return unique_filename
    return None

def save_uploaded_cv(file):
    """Save uploaded CV file and return the filename"""
    if file and allowed_cv_file(file.filename):
        filename = secure_filename(file.filename)
        # Generate unique filename
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(app.config['CV_UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        return unique_filename
    return None

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# ======================
# DASHBOARD
# ======================
@app.route('/')
@login_required
def index():

    search = request.args.get('q')
    status = request.args.get('status')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Show 10 records per page
    statuses = Status.query.all()

    query = JobApplication.query.filter_by(user_id=current_user.id)

    if search:
        query = query.filter(
            JobApplication.company_name.ilike(f'%{search}%')
        )

    if status and status != 'All':
        query = query.filter(
            JobApplication.status.has(name=status)
        )

    # Filter berdasarkan rentang tanggal
    if start_date:
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            query = query.filter(JobApplication.applied_date >= start_date_obj)
        except ValueError:
            pass

    if end_date:
        try:
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            # Include the entire end date by adding 1 day and filtering less than
            end_date_obj = end_date_obj.replace(day=end_date_obj.day + 1)
            query = query.filter(JobApplication.applied_date < end_date_obj)
        except ValueError:
            pass

    # Paginate the results
    pagination = query.order_by(JobApplication.applied_date.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    jobs = pagination.items


    # 📊 DASHBOARD PER USER
    total = JobApplication.query.filter_by(user_id=current_user.id).count()
    terdaftar = JobApplication.query.filter(
        JobApplication.user_id == current_user.id,
        JobApplication.status.has(name='Terdaftar')
    ).count()
    interview = JobApplication.query.filter(
        JobApplication.user_id == current_user.id,
        JobApplication.status.has(name='Interview')
    ).count()

    tes = JobApplication.query.filter(
        JobApplication.user_id == current_user.id,
        JobApplication.status.has(name='Tes')
    ).count()

    diterima = JobApplication.query.filter(
        JobApplication.user_id == current_user.id,
        JobApplication.status.has(name='Diterima')
    ).count()

    ditolak = JobApplication.query.filter(
        JobApplication.user_id == current_user.id,
        JobApplication.status.has(name='Tidak Diterima')
    ).count()



    return render_template(
        'index.html',
        jobs=jobs,
        statuses=statuses,
        total=total,
        terdaftar=terdaftar,
        interview=interview,
        tes=tes,
        diterima=diterima,
        ditolak=ditolak,
        pagination=pagination
    )



# ======================
# ADD JOB
# ======================
@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_job():


    if request.method == 'POST':
        # Handle image upload
        image_proof = None
        if 'image_proof' in request.files:
            file = request.files['image_proof']
            if file.filename:
                image_proof = save_uploaded_image(file)
        
        # Handle applied_date - if not provided, use current date
        applied_date = datetime.now()
        if request.form.get('applied_date'):
            try:
                applied_date = datetime.strptime(request.form['applied_date'], '%Y-%m-%d')
            except ValueError:
                applied_date = datetime.now()


        # Handle source_info - if custom, use the custom input
        source_info = request.form.get('source_info', '')
        if source_info == 'Custom':
            source_info = request.form.get('custom_source', '')
        

        job = JobApplication(
            company_name=request.form['company_name'],
            position=request.form.get('position', ''),  # NEW: Handle posisi
            location=request.form['location'],
            address=request.form['address'],
            application_proof=request.form.get('application_proof', ''),  # NEW: Handle bukti
            image_proof=image_proof,  # NEW: Handle uploaded image
            source_info=source_info,  # Handle custom source_info
            status_id=request.form['status_id'],  # ✅ INI PENTING
            applied_date=applied_date,
            last_status_update=applied_date,  # NEW: Set tanggal update awal sama dengan applied_date
            user_id=current_user.id
        )
        db.session.add(job)
        db.session.commit()
        return redirect(url_for('index'))

    statuses = Status.query.all()
    return render_template('add.html', statuses=statuses)

# ======================
# EDIT JOB
# ======================
@app.route('/job/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    job = JobApplication.query.get_or_404(id)

    if job.user_id != current_user.id:
        abort(403)

    statuses = Status.query.all()




    if request.method == 'POST':


        job.company_name = request.form['company_name']
        job.position = request.form.get('position', '')  # NEW: Handle posisi
        job.location = request.form['location']
        job.address = request.form['address']
        job.application_proof = request.form.get('application_proof', '')  # NEW: Handle bukti
        
        # Handle source_info - if custom, use the custom input
        source_info = request.form.get('source_info', '')
        if source_info == 'Custom':
            source_info = request.form.get('custom_source', '')
        job.source_info = source_info
        
        # Handle applied_date - if provided, update the date
        if request.form.get('applied_date'):
            try:
                job.applied_date = datetime.strptime(request.form['applied_date'], '%Y-%m-%d')
            except ValueError:
                pass  # Keep existing date if invalid
        
        # Handle image upload
        if 'image_proof' in request.files:
            file = request.files['image_proof']
            if file.filename:
                # Save new image
                new_image = save_uploaded_image(file)
                if new_image:
                    # Delete old image if exists
                    if job.image_proof:
                        old_file_path = os.path.join(app.config['UPLOAD_FOLDER'], job.image_proof)
                        if os.path.exists(old_file_path):
                            os.remove(old_file_path)
                    job.image_proof = new_image
        

        old_status_id = job.status_id
        new_status_id = int(request.form['status_id'])
        
        job.status_id = new_status_id
        
        # NEW: Update tanggal status jika status berubah
        if old_status_id != new_status_id:
            job.last_status_update = datetime.now()
        
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit.html', job=job, statuses=statuses)


# ======================
# LOGIN
# ======================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(
            username=request.form['username']
        ).first()

        if user and check_password_hash(
            user.password,
            request.form['password']
        ):
            login_user(user)
            return redirect(url_for('index'))

        flash('Username atau password salah', 'danger')

    return render_template('login.html')










# ======================
# UPDATE STATUS AJAX
# ======================
@app.route('/update_status/<int:job_id>', methods=['POST'])
@login_required
def update_status(job_id):
    try:
        job = JobApplication.query.get_or_404(job_id)
        
        if job.user_id != current_user.id:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
        
        data = request.get_json()
        if not data or 'status_id' not in data:
            return jsonify({'success': False, 'error': 'Invalid data'}), 400
        

        job.status_id = data['status_id']
        job.last_status_update = datetime.now()  # NEW: Update tanggal status terakhir berubah
        db.session.commit()
        

        # Calculate updated statistics
        total = JobApplication.query.filter_by(user_id=current_user.id).count()
        terdaftar = JobApplication.query.filter(
            JobApplication.user_id == current_user.id,
            JobApplication.status.has(name='Terdaftar')
        ).count()
        interview = JobApplication.query.filter(
            JobApplication.user_id == current_user.id,
            JobApplication.status.has(name='Interview')
        ).count()
        tes = JobApplication.query.filter(
            JobApplication.user_id == current_user.id,
            JobApplication.status.has(name='Tes')
        ).count()
        diterima = JobApplication.query.filter(
            JobApplication.user_id == current_user.id,
            JobApplication.status.has(name='Diterima')
        ).count()
        ditolak = JobApplication.query.filter(
            JobApplication.user_id == current_user.id,
            JobApplication.status.has(name='Tidak Diterima')
        ).count()
        
        return jsonify({
            'success': True,
            'stats': {
                'total': total,
                'terdaftar': terdaftar,
                'interview': interview,
                'tes': tes,
                'diterima': diterima,
                'ditolak': ditolak
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ======================
# UPDATE STATUS VIA STRING (NEW API)
# ======================
@app.route('/api/job/<int:job_id>/status', methods=['POST'])
@login_required
def update_job_status(job_id):
    """API endpoint untuk update status menggunakan string status"""
    try:
        job = JobApplication.query.get_or_404(job_id)
        
        if job.user_id != current_user.id:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        data = request.get_json()
        if not data or 'status' not in data:
            return jsonify({'success': False, 'message': 'Invalid data'}), 400
        
        status_name = data['status']
        
        # Find status by name
        status = Status.query.filter_by(name=status_name).first()
        if not status:
            return jsonify({'success': False, 'message': 'Status tidak ditemukan'}), 400
        


        # Update job status
        job.status_id = status.id
        job.last_status_update = datetime.now()  # NEW: Update tanggal status terakhir berubah
        db.session.commit()
        
        # Create notification for status change
        notification_title = "Status Lamaran Diupdate"
        notification_message = f"Status lamaran di {job.company_name} berhasil diubah menjadi {status_name}"
        notification_type = "info"
        
        # Set notification type based on status
        if status_name == "Diterima":
            notification_type = "success"
            notification_title = "🎉 Selamat! Lamaran Diterima!"
            notification_message = f"Selamat! Lamaran Anda di {job.company_name} untuk posisi {job.position or 'Posisi'} telah diterima!"
        elif status_name == "Tidak Diterima":
            notification_type = "warning"
            notification_title = "Lamaran Tidak Diterima"
            notification_message = f"Maaf, lamaran Anda di {job.company_name} untuk posisi {job.position or 'Posisi'} tidak diterima. Jangan menyerah!"
        elif status_name == "Interview":
            notification_type = "info"
            notification_title = "📞 Undangan Interview"
            notification_message = f"Anda mendapat undangan interview untuk posisi {job.position or 'Posisi'} di {job.company_name}. Persiapkan diri dengan baik!"
        elif status_name == "Tes":
            notification_type = "info"
            notification_title = "📝 Undangan Tes"
            notification_message = f"Anda mendapat undangan tes untuk posisi {job.position or 'Posisi'} di {job.company_name}. Belajar dan persiapan yang matang!"
        
        # Create notification record
        notification = Notification(
            user_id=current_user.id,
            title=notification_title,
            message=notification_message,
            type=notification_type,
            job_id=job.id
        )
        db.session.add(notification)
        db.session.commit()
        
        # Calculate updated statistics
        total = JobApplication.query.filter_by(user_id=current_user.id).count()
        terdaftar = JobApplication.query.filter(
            JobApplication.user_id == current_user.id,
            JobApplication.status.has(name='Terdaftar')
        ).count()
        interview = JobApplication.query.filter(
            JobApplication.user_id == current_user.id,
            JobApplication.status.has(name='Interview')
        ).count()
        tes = JobApplication.query.filter(
            JobApplication.user_id == current_user.id,
            JobApplication.status.has(name='Tes')
        ).count()
        diterima = JobApplication.query.filter(
            JobApplication.user_id == current_user.id,
            JobApplication.status.has(name='Diterima')
        ).count()
        ditolak = JobApplication.query.filter(
            JobApplication.user_id == current_user.id,
            JobApplication.status.has(name='Tidak Diterima')
        ).count()
        
        return jsonify({
            'success': True,
            'message': 'Status berhasil diupdate',
            'stats': {
                'total': total,
                'terdaftar': terdaftar,
                'interview': interview,
                'tes': tes,
                'diterima': diterima,
                'ditolak': ditolak
            }
        })
        
    except Exception as e:
        print(f"Error updating status: {str(e)}")

        return jsonify({'success': False, 'message': str(e)}), 500

# ======================
# NOTIFICATION SYSTEM API
# ======================

@app.route('/api/notifications')
@login_required
def get_notifications():
    """API endpoint untuk mendapatkan notifikasi user"""
    try:
        notifications = Notification.query.filter_by(user_id=current_user.id)\
            .order_by(Notification.created_at.desc())\
            .limit(20).all()
        
        notifications_data = []
        for notif in notifications:
            notifications_data.append({
                'id': notif.id,
                'title': notif.title,
                'message': notif.message,
                'type': notif.type,
                'is_read': notif.is_read,
                'created_at': notif.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'job_id': notif.job_id
            })
        
        # Get unread count
        unread_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
        
        return jsonify({
            'success': True,
            'notifications': notifications_data,
            'unread_count': unread_count
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/notifications/<int:notification_id>/read', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    """API endpoint untuk menandai notifikasi sebagai dibaca"""
    try:
        notification = Notification.query.filter_by(
            id=notification_id, 
            user_id=current_user.id
        ).first()
        
        if not notification:
            return jsonify({'success': False, 'error': 'Notifikasi tidak ditemukan'}), 404
        
        notification.is_read = True
        db.session.commit()
        
        # Get updated unread count
        unread_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
        
        return jsonify({
            'success': True,
            'message': 'Notifikasi berhasil ditandai sebagai dibaca',
            'unread_count': unread_count
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/notifications/mark_all_read', methods=['POST'])
@login_required
def mark_all_notifications_read():
    """API endpoint untuk menandai semua notifikasi sebagai dibaca"""
    try:
        unread_notifications = Notification.query.filter_by(
            user_id=current_user.id, 
            is_read=False
        ).all()
        
        for notification in unread_notifications:
            notification.is_read = True
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{len(unread_notifications)} notifikasi berhasil ditandai sebagai dibaca',
            'unread_count': 0
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/notifications/<int:notification_id>', methods=['DELETE'])
@login_required
def delete_notification(notification_id):
    """API endpoint untuk menghapus notifikasi"""
    try:
        notification = Notification.query.filter_by(
            id=notification_id, 
            user_id=current_user.id
        ).first()
        
        if not notification:
            return jsonify({'success': False, 'error': 'Notifikasi tidak ditemukan'}), 404
        
        db.session.delete(notification)
        db.session.commit()
        
        # Get updated unread count
        unread_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
        
        return jsonify({
            'success': True,
            'message': 'Notifikasi berhasil dihapus',
            'unread_count': unread_count
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/notifications/clear_all', methods=['DELETE'])
@login_required
def clear_all_notifications():
    """API endpoint untuk menghapus semua notifikasi"""
    try:
        # Delete all notifications for current user
        deleted_count = Notification.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{deleted_count} notifikasi berhasil dihapus',
            'unread_count': 0
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500





# ======================
# AI-POWERED FEATURES
# ======================

# Initialize AI services
ai_service = AIService()
cv_analyzer = CVAnalyzer()
job_matcher = JobMatcher()
insights_generator = InsightsGenerator()

# CV Upload and Analysis

@app.route('/ai/cv/upload', methods=['GET', 'POST'])
@login_required
def upload_cv():
    """Upload and analyze CV/Resume"""
    if request.method == 'POST':
        try:
            # Handle file upload
            if 'cv_file' not in request.files:
                return jsonify({'success': False, 'error': 'No file provided'}), 400
            
            file = request.files['cv_file']
            if file.filename == '':
                return jsonify({'success': False, 'error': 'No file selected'}), 400
            
            # Save uploaded CV file using the new function
            cv_filename = save_uploaded_cv(file)
            if not cv_filename:
                return jsonify({'success': False, 'error': 'Invalid file type. Please upload PDF, DOC, DOCX, or TXT files only.'}), 400
            
            # Read file content for analysis
            file_path = os.path.join(app.config['CV_UPLOAD_FOLDER'], cv_filename)
            
            # Handle different file types
            file_extension = file.filename.rsplit('.', 1)[1].lower()
            cv_content = ""
            
            try:
                if file_extension == 'pdf':
                    # For PDF files, we'll use a simple text extraction (in real app, use PyPDF2 or similar)
                    with open(file_path, 'rb') as f:
                        cv_content = f.read().decode('utf-8', errors='ignore')
                elif file_extension in ['doc', 'docx']:
                    # For DOC/DOCX files, use python-docx or similar library
                    with open(file_path, 'rb') as f:
                        cv_content = f.read().decode('utf-8', errors='ignore')
                else:
                    # For TXT files
                    with open(file_path, 'r', encoding='utf-8') as f:
                        cv_content = f.read()
            except Exception as e:
                print(f"Error reading file: {str(e)}")
                return jsonify({'success': False, 'error': 'Error reading file content. Please make sure the file is not corrupted.'}), 400
            
            # Analyze CV using AI
            analysis_result = cv_analyzer.analyze_cv(cv_content)
            
            # Save or update CV profile
            cv_profile = CVProfile.query.filter_by(user_id=current_user.id).first()
            if not cv_profile:
                cv_profile = CVProfile(user_id=current_user.id)
                db.session.add(cv_profile)
            
            # Update CV profile with analysis results
            cv_profile.cv_file_path = cv_filename
            cv_profile.file_size = len(cv_content)
            cv_profile.full_name = analysis_result.get('personal_info', {}).get('name', '')
            cv_profile.email = analysis_result.get('personal_info', {}).get('email', '')
            cv_profile.phone = analysis_result.get('personal_info', {}).get('phone', '')
            cv_profile.location = analysis_result.get('personal_info', {}).get('location', '')
            cv_profile.extracted_skills = json.dumps(analysis_result.get('skills', []))
            cv_profile.experience_level = analysis_result.get('experience_level', 'unknown')
            cv_profile.years_experience = analysis_result.get('years_experience', 0)
            cv_profile.education_level = analysis_result.get('education_level', '')
            cv_profile.summary = analysis_result.get('summary', '')
            cv_profile.ats_score = analysis_result.get('ats_score', 0)
            cv_profile.completeness_score = analysis_result.get('completeness_score', 0)
            cv_profile.last_updated = datetime.now()
            
            db.session.commit()
            
            # Generate insights based on CV analysis
            user_data = {
                'cv_analysis': analysis_result,
                'job_applications': []
            }
            insights = insights_generator.generate_all_insights(user_data)
            
            # Save insights to database
            for insight in insights:
                ai_insight = AIInsight(
                    user_id=current_user.id,
                    insight_type=insight['type'],
                    title=insight['title'],
                    content=insight['content'],
                    confidence_score=insight.get('confidence', 0),
                    priority_level=insight.get('priority', 3),
                    action_required=insight.get('action_required', False),
                    action_text=insight.get('action_text', ''),
                    related_skills=json.dumps(insight.get('related_skills', []))
                )
                db.session.add(ai_insight)
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'CV analyzed successfully',
                'analysis': analysis_result,
                'insights_count': len(insights)
            })
            
        except Exception as e:
            print(f"CV Analysis Error: {str(e)}")
            print(traceback.format_exc())
            return jsonify({'success': False, 'error': str(e)}), 500
    
    return render_template('cv_upload.html')

# AI Dashboard
@app.route('/ai/dashboard')
@login_required
def ai_dashboard():
    """AI-powered insights dashboard"""
    try:
        # Get user's CV profile
        cv_profile = CVProfile.query.filter_by(user_id=current_user.id).first()
        
        # Get AI insights
        insights = AIInsight.query.filter_by(user_id=current_user.id)\
            .order_by(AIInsight.created_at.desc()).limit(10).all()
        
        # Get job matches
        job_matches = JobMatch.query.filter_by(user_id=current_user.id)\
            .order_by(JobMatch.match_score.desc()).limit(5).all()
        
        # Get skill gaps
        skill_gaps = SkillGap.query.filter_by(user_id=current_user.id)\
            .order_by(SkillGap.priority_score.desc()).limit(10).all()
        
        # Get career trajectories
        career_trajectories = CareerTrajectory.query.filter_by(user_id=current_user.id)\
            .order_by(CareerTrajectory.created_at.desc()).limit(3).all()
        
        return render_template('ai_dashboard.html',
                             cv_profile=cv_profile,
                             insights=insights,
                             job_matches=job_matches,
                             skill_gaps=skill_gaps,
                             career_trajectories=career_trajectories)
        
    except Exception as e:
        print(f"AI Dashboard Error: {str(e)}")
        flash('Error loading AI dashboard', 'danger')
        return redirect(url_for('index'))

# Job Matching API
@app.route('/api/ai/job-match/<int:job_id>', methods=['POST'])
@login_required
def match_job(job_id):
    """Match a specific job with user's CV"""
    try:
        job = JobApplication.query.get_or_404(job_id)
        
        if job.user_id != current_user.id:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
        
        # Get user's CV profile
        cv_profile = CVProfile.query.filter_by(user_id=current_user.id).first()
        if not cv_profile:
            return jsonify({'success': False, 'error': 'No CV profile found. Please upload your CV first.'}), 400
        
        # Parse CV skills
        cv_skills = json.loads(cv_profile.extracted_skills) if cv_profile.extracted_skills else []
        
        # Create job description from job data
        job_description = f"""
        Position: {job.position}
        Company: {job.company_name}
        Location: {job.location}
        Requirements: {job.application_proof}
        """
        
        # Perform job matching
        match_result = job_matcher.match_job(cv_skills, job_description)
        
        # Save match result
        job_match = JobMatch(
            user_id=current_user.id,
            job_id=job.id,
            match_score=match_result['match_score'],
            matching_skills=json.dumps(match_result['matching_skills']),
            missing_skills=json.dumps(match_result['missing_skills']),
            additional_skills=json.dumps(match_result['additional_skills']),
            compatibility_factors=json.dumps(match_result['compatibility_factors']),
            recommendations=match_result['recommendations'],
            salary_match_score=match_result.get('salary_match_score', 0),
            location_match_score=match_result.get('location_match_score', 0)
        )
        
        # Remove existing match for this job
        existing_match = JobMatch.query.filter_by(user_id=current_user.id, job_id=job.id).first()
        if existing_match:
            db.session.delete(existing_match)
        
        db.session.add(job_match)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'match_result': match_result,
            'message': 'Job matching completed successfully'
        })
        
    except Exception as e:
        print(f"Job Matching Error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'success': False, 'error': str(e)}), 500

# Generate All Insights
@app.route('/api/ai/generate-insights', methods=['POST'])
@login_required
def generate_insights():
    """Generate AI insights for user"""
    try:
        # Get user data
        cv_profile = CVProfile.query.filter_by(user_id=current_user.id).first()
        job_applications = JobApplication.query.filter_by(user_id=current_user.id).all()
        
        # Prepare user data for insights generation
        user_data = {
            'cv_analysis': {
                'extracted_skills': json.loads(cv_profile.extracted_skills) if cv_profile and cv_profile.extracted_skills else [],
                'experience_level': cv_profile.experience_level if cv_profile else 'unknown',
                'years_experience': cv_profile.years_experience if cv_profile else 0,
                'ats_score': cv_profile.ats_score if cv_profile else 0
            },
            'job_applications': [{
                'position': job.position,
                'company_name': job.company_name,
                'location': job.location,
                'status': job.status.name if job.status else 'Unknown'
            } for job in job_applications]
        }
        
        # Generate insights
        insights = insights_generator.generate_all_insights(user_data)
        
        # Clear existing insights
        AIInsight.query.filter_by(user_id=current_user.id).delete()
        
        # Save new insights
        saved_insights = []
        for insight in insights:
            ai_insight = AIInsight(
                user_id=current_user.id,
                insight_type=insight['type'],
                title=insight['title'],
                content=insight['content'],
                confidence_score=insight.get('confidence', 0),
                priority_level=insight.get('priority', 3),
                action_required=insight.get('action_required', False),
                action_text=insight.get('action_text', ''),
                related_skills=json.dumps(insight.get('related_skills', []))
            )
            db.session.add(ai_insight)
            saved_insights.append(ai_insight)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Generated {len(saved_insights)} insights successfully',
            'insights_count': len(saved_insights)
        })
        
    except Exception as e:
        print(f"Generate Insights Error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'success': False, 'error': str(e)}), 500

# AI Insights API
@app.route('/api/ai/insights')
@login_required
def get_ai_insights():
    """Get AI insights for user"""
    try:
        insights = AIInsight.query.filter_by(user_id=current_user.id)\
            .order_by(AIInsight.priority_level.desc(), AIInsight.created_at.desc())\
            .limit(20).all()
        
        insights_data = []
        for insight in insights:
            insights_data.append({
                'id': insight.id,
                'type': insight.insight_type,
                'title': insight.title,
                'content': insight.content,
                'confidence_score': insight.confidence_score,
                'priority_level': insight.priority_level,
                'is_read': insight.is_read,
                'action_required': insight.action_required,
                'action_text': insight.action_text,
                'related_skills': json.loads(insight.related_skills) if insight.related_skills else [],
                'created_at': insight.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return jsonify({
            'success': True,
            'insights': insights_data
        })
        
    except Exception as e:
        print(f"Get AI Insights Error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ======================
# SERVE UPLOADED IMAGE
# ======================
@app.route('/uploads/proofs/<filename>')
def uploaded_file(filename):
    """Serve uploaded proof images"""
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))



# ======================
# SIDEBAR NAVIGATION PAGES
# ======================

# Jobs List Page
@app.route('/jobs')
@login_required
def jobs():
    """Halaman daftar lamaran kerja dengan fitur pencarian dan filter"""
    search = request.args.get('q', '')
    status = request.args.get('status', 'All')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    statuses = Status.query.all()
    query = JobApplication.query.filter_by(user_id=current_user.id)

    if search:
        query = query.filter(
            JobApplication.company_name.ilike(f'%{search}%')
        )

    if status and status != 'All':
        query = query.filter(
            JobApplication.status.has(name=status)
        )

    # Filter berdasarkan rentang tanggal
    if start_date:
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            query = query.filter(JobApplication.applied_date >= start_date_obj)
        except ValueError:
            pass

    if end_date:
        try:
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            end_date_obj = end_date_obj.replace(day=end_date_obj.day + 1)
            query = query.filter(JobApplication.applied_date < end_date_obj)
        except ValueError:
            pass

    pagination = query.order_by(JobApplication.applied_date.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    jobs = pagination.items

    return render_template('jobs.html', 
                         jobs=jobs, 
                         statuses=statuses, 
                         pagination=pagination,
                         search=search,
                         selected_status=status,
                         start_date=start_date,
                         end_date=end_date)

# Reports & Export Page
@app.route('/reports')
@login_required
def reports():
    """Halaman laporan dan export data"""
    # Get statistics for current user
    total = JobApplication.query.filter_by(user_id=current_user.id).count()
    terdaftar = JobApplication.query.filter(
        JobApplication.user_id == current_user.id,
        JobApplication.status.has(name='Terdaftar')
    ).count()
    interview = JobApplication.query.filter(
        JobApplication.user_id == current_user.id,
        JobApplication.status.has(name='Interview')
    ).count()
    tes = JobApplication.query.filter(
        JobApplication.user_id == current_user.id,
        JobApplication.status.has(name='Tes')
    ).count()
    diterima = JobApplication.query.filter(
        JobApplication.user_id == current_user.id,
        JobApplication.status.has(name='Diterima')
    ).count()
    ditolak = JobApplication.query.filter(
        JobApplication.user_id == current_user.id,
        JobApplication.status.has(name='Tidak Diterima')
    ).count()

    # Calculate success rate
    success_rate = 0
    if total > 0:
        success_rate = round((diterima / total) * 100, 1)

    return render_template('reports.html',
                         total=total,
                         terdaftar=terdaftar,
                         interview=interview,
                         tes=tes,
                         diterima=diterima,
                         ditolak=ditolak,
                         success_rate=success_rate)

# Settings Page
@app.route('/settings')
@login_required
def settings():
    """Halaman pengaturan aplikasi"""
    # Get current user statistics
    total_jobs = JobApplication.query.filter_by(user_id=current_user.id).count()
    
    # Get database file size
    db_path = 'instance/database.db'
    db_size = 0
    if os.path.exists(db_path):
        db_size = os.path.getsize(db_path)
    
    return render_template('settings.html',
                         total_jobs=total_jobs,
                         db_size=db_size)


# Help Page
@app.route('/help')
@login_required
def help():
    """Halaman bantuan dan panduan penggunaan"""
    return render_template('help.html')

# ======================
# DELETE JOB
# ======================
@app.route('/job/<int:id>/delete', methods=['POST'])
@login_required
def delete_job(id):
    job = JobApplication.query.get_or_404(id)
    
    if job.user_id != current_user.id:
        abort(403)
    
    # Delete associated image file if exists
    if job.image_proof:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], job.image_proof)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    db.session.delete(job)
    db.session.commit()
    
    return {'success': True, 'message': 'Job berhasil dihapus'}



# ======================
# EXPORT PDF
# ======================
@app.route('/export/pdf')
@login_required
def export_pdf():
    """Export job applications to PDF"""
    try:
        # Get all jobs for current user
        jobs = JobApplication.query.filter_by(user_id=current_user.id).order_by(JobApplication.applied_date.desc()).all()
        
        if not jobs:
            flash('Tidak ada data untuk diekspor', 'warning')
            return redirect(url_for('index'))
        
        # Create PDF buffer
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            textColor=colors.darkblue
        )
        
        # Add title
        title = Paragraph("Laporan Lamaran Kerja", title_style)
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Add generation date
        date_str = f"Tanggal Generate: {datetime.now().strftime('%d %B %Y, %H:%M')}"
        story.append(Paragraph(date_str, styles['Normal']))
        story.append(Spacer(1, 30))
        

        # Create table data
        table_data = [
            ['No', 'Perusahaan', 'Posisi', 'Lokasi', 'Status', 'Tanggal Apply', 'Terakhir Diupdate', 'Sumber Info']
        ]
        

        for idx, job in enumerate(jobs, 1):
            table_data.append([
                str(idx),
                job.company_name or '-',
                job.position or '-',
                job.location or '-',
                job.status.name if job.status else '-',
                job.applied_date.strftime('%d/%m/%Y') if job.applied_date else '-',
                job.last_status_update.strftime('%d/%m/%Y %H:%M') if job.last_status_update else '-',
                job.source_info or '-'
            ])
        
        # Create table
        table = Table(table_data, colWidths=[0.5*inch, 1.5*inch, 1.2*inch, 1*inch, 1*inch, 1*inch, 1*inch])
        
        # Style the table
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        story.append(table)
        
        # Add summary
        story.append(Spacer(1, 30))
        summary_text = f"""
        <b>Ringkasan:</b><br/>
        Total Lamaran: {len(jobs)}<br/>
        Status Terdaftar: {len([j for j in jobs if j.status.name == 'Terdaftar'])}<br/>
        Status Interview: {len([j for j in jobs if j.status.name == 'Interview'])}<br/>
        Status Tes: {len([j for j in jobs if j.status.name == 'Tes'])}<br/>
        Status Diterima: {len([j for j in jobs if j.status.name == 'Diterima'])}<br/>
        Status Tidak Diterima: {len([j for j in jobs if j.status.name == 'Tidak Diterima'])}
        """
        summary = Paragraph(summary_text, styles['Normal'])
        story.append(summary)
        
        # Build PDF
        doc.build(story)
        
        # Prepare response
        buffer.seek(0)
        filename = f"laporan_lamaran_kerja_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        return Response(
            buffer.getvalue(),
            mimetype='application/pdf',
            headers={
                'Content-Disposition': f'attachment; filename="{filename}"',
                'Content-Type': 'application/pdf'
            }
        )
        
    except Exception as e:
        flash(f'Error dalam export PDF: {str(e)}', 'danger')
        return redirect(url_for('index'))

# ======================
# EXPORT EXCEL
# ======================
@app.route('/export/excel')
@login_required
def export_excel():
    """Export job applications to Excel"""
    try:
        # Get all jobs for current user
        jobs = JobApplication.query.filter_by(user_id=current_user.id).order_by(JobApplication.applied_date.desc()).all()
        
        if not jobs:
            flash('Tidak ada data untuk diekspor', 'warning')
            return redirect(url_for('index'))
        

        # Prepare data for DataFrame
        data = []
        for job in jobs:
            data.append({
                'No': len(data) + 1,
                'Nama Perusahaan': job.company_name or '-',
                'Posisi': job.position or '-',
                'Lokasi': job.location or '-',
                'Alamat': job.address or '-',
                'Status': job.status.name if job.status else '-',
                'Tanggal Apply': job.applied_date.strftime('%d/%m/%Y') if job.applied_date else '-',
                'Terakhir Diupdate': job.last_status_update.strftime('%d/%m/%Y %H:%M') if job.last_status_update else '-',
                'Sumber Info': job.source_info or '-',
                'Bukti Lamaran (Link)': job.application_proof or '-',
                'Catatan': job.notes or '-'
            })
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Create Excel buffer
        buffer = BytesIO()
        
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            # Write main data
            df.to_excel(writer, sheet_name='Data Lamaran Kerja', index=False)
            
            # Get workbook and worksheet
            workbook = writer.book
            worksheet = writer.sheets['Data Lamaran Kerja']
            
            # Auto-adjust column widths
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
            

            # Create summary sheet
            summary_data = [
                ['Keterangan', 'Jumlah'],
                ['Ringkasan Data Lamaran Kerja', ''],
                ['', ''],
                ['Total Lamaran', len(jobs)],
                ['Status Terdaftar', len([j for j in jobs if j.status.name == 'Terdaftar'])],
                ['Status Interview', len([j for j in jobs if j.status.name == 'Interview'])],
                ['Status Tes', len([j for j in jobs if j.status.name == 'Tes'])],
                ['Status Diterima', len([j for j in jobs if j.status.name == 'Diterima'])],
                ['Status Tidak Diterima', len([j for j in jobs if j.status.name == 'Tidak Diterima'])],
                ['', ''],
                ['Tanggal Export', datetime.now().strftime('%d/%m/%Y %H:%M:%S')],
                ['User', current_user.username]
            ]
            
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Ringkasan', index=False)
            
            # Style the summary sheet
            summary_ws = writer.sheets['Ringkasan']
            summary_ws['A1'].font = summary_ws['A1'].font.copy(bold=True, size=14)
        
        buffer.seek(0)
        filename = f"data_lamaran_kerja_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        return Response(
            buffer.getvalue(),
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={
                'Content-Disposition': f'attachment; filename="{filename}"',
                'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            }
        )
        
    except Exception as e:
        flash(f'Error dalam export Excel: {str(e)}', 'danger')
        return redirect(url_for('index'))

# ======================
# LOGOUT
# ======================
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
