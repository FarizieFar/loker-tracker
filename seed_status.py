from app import app, db
from models import Status

with app.app_context():
    statuses = [
        ('Terdaftar', 'secondary'),
        ('Interview', 'warning'),
        ('Tes', 'info'),
        ('Diterima', 'success'),
        ('Tidak Diterima', 'danger')
    ]

    for name, color in statuses:
        db.session.add(Status(name=name, color=color))

    db.session.commit()

print("Status berhasil diisi")
