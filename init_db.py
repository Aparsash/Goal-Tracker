# init_db.py
from app import app, db

# Run this only once to create all tables
with app.app_context():
    db.create_all()
    print("✅ Tables created successfully.")
