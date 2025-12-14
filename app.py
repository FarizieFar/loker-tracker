

from flask import Flask, render_template, redirect, url_for, request, flash, abort, jsonify, send_file
from datetime import datetime
from extensions import db
from models import JobApplication, User, Status
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
import os
import uuid


app = Flask(__name__)


app.config['SECRET_KEY'] = 'super-secret-key-alfarizi'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# File upload configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads/proofs'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}



# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

    jobs = query.order_by(JobApplication.applied_date.desc()).all()


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
        ditolak=ditolak
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
        

        job = JobApplication(
            company_name=request.form['company_name'],
            position=request.form.get('position', ''),  # NEW: Handle posisi
            location=request.form['location'],
            address=request.form['address'],
            application_proof=request.form.get('application_proof', ''),  # NEW: Handle bukti
            image_proof=image_proof,  # NEW: Handle uploaded image
            source_info=request.form.get('source_info', ''),  # NEW: Handle asal info loker
            status_id=request.form['status_id'],  # ✅ INI PENTING
            applied_date=datetime.now(),
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
        job.source_info = request.form.get('source_info', '')  # NEW: Handle asal info loker
        
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
        
        job.status_id = request.form['status_id']
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
# SERVE UPLOADED IMAGE
# ======================
@app.route('/uploads/proofs/<filename>')
def uploaded_file(filename):
    """Serve uploaded proof images"""
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))


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
    app.run(debug=True)
