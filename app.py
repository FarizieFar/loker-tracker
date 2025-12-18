



from flask import Flask, render_template, redirect, url_for, request, flash, abort, jsonify, send_file, Response
from datetime import datetime, date
from extensions import db
from models import JobApplication, User, Status
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
            ['No', 'Perusahaan', 'Posisi', 'Lokasi', 'Status', 'Tanggal Apply', 'Sumber Info']
        ]
        
        for idx, job in enumerate(jobs, 1):
            table_data.append([
                str(idx),
                job.company_name or '-',
                job.position or '-',
                job.location or '-',
                job.status.name if job.status else '-',
                job.applied_date.strftime('%d/%m/%Y') if job.applied_date else '-',
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
