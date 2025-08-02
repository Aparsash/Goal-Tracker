#models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)

    goals = relationship('Goal', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Goal(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    total_units = Column(Float, nullable=False)
    daily_target = Column(Float, nullable=False)
    target_date = Column(Date, nullable=False)

    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    progress_entries = relationship('ProgressEntry', backref='goal', lazy=True, cascade='all, delete-orphan')

class ProgressEntry(db.Model):
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    value = Column(Float, nullable=False)

    goal_id = Column(Integer, ForeignKey('goal.id', ondelete='CASCADE'), nullable=False)