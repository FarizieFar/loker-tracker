from app import app, db
from models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    user = User(
        username="fariz",
        password=generate_password_hash("fariz123")
    )
    db.session.add(user)
    db.session.commit()

print("Admin berhasil dibuat")
