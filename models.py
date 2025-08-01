# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# === Define db as a placeholder ===
db = SQLAlchemy()

class User(db.Model, UserMixin):
    """User model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    # One-to-many relationship with Goal
    goals = db.relationship('Goal', backref='owner', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        """Hash and store the password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the entered password is correct"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email}>"


class Goal(db.Model):
    """Goal model"""
    __tablename__ = 'goals'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    total_units = db.Column(db.Float, nullable=False)
    target_date = db.Column(db.Date, nullable=False)
    daily_target = db.Column(db.Float, nullable=False)
    
    # Foreign Key to User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # One-to-many relationship with ProgressEntry
    progress_entries = db.relationship('ProgressEntry', backref='goal', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Goal {self.title} (ID: {self.id}) for User ID {self.user_id}>"


class ProgressEntry(db.Model):
    """Daily progress entry model"""
    __tablename__ = 'progress_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    value = db.Column(db.Float, nullable=False)
    
    # Foreign Key to Goal
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.id'), nullable=False)

    def __repr__(self):
        return f"<ProgressEntry ID {self.id} on {self.date}: {self.value} for Goal ID {self.goal_id}>"
