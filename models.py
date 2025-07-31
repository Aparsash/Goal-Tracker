# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# این db باید بعداً از app.py ایمپورت بشه.
# فعلاً برای جلوگیری از خطا، یه placeholder می‌زاریم.
# db = SQLAlchemy() # این خط رو بعداً فعال می‌کنیم.

# === برای تست اولیه، یه نمونه موقت از SQLAlchemy می‌سازیم ===
# (در عمل، این نیاز نیست)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy as _BaseSQLAlchemy

class SQLAlchemy(_BaseSQLAlchemy):
    def apply_pool_defaults(self, app, options):
        options.setdefault('pool_pre_ping', True)
        super().apply_pool_defaults(app, options)

# این فقط برای تست اولیه هست و بعداً حذف می‌شه
app_test = Flask(__name__)
app_test.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app_test.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app_test)
# === پایان بخش موقت ===


class User(db.Model, UserMixin):
    """مدل کاربر"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    # رابطه یک به چند با Goal
    goals = db.relationship('Goal', backref='owner', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        """رمز عبور رو هش می‌کنه و ذخیره می‌کنه."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """چک می‌کنه رمز وارد شده درست هست یا نه."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email}>"


class Goal(db.Model):
    """مدل هدف"""
    __tablename__ = 'goals'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    total_units = db.Column(db.Float, nullable=False)
    target_date = db.Column(db.Date, nullable=False)
    daily_target = db.Column(db.Float, nullable=False)
    
    # Foreign Key به User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # رابطه یک به چند با ProgressEntry
    progress_entries = db.relationship('ProgressEntry', backref='goal', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Goal {self.title} (ID: {self.id}) for User ID {self.user_id}>"


class ProgressEntry(db.Model):
    """مدل پیشرفت روزانه"""
    __tablename__ = 'progress_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    value = db.Column(db.Float, nullable=False)
    
    # Foreign Key به Goal
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.id'), nullable=False)

    def __repr__(self):
        return f"<ProgressEntry ID {self.id} on {self.date}: {self.value} for Goal ID {self.goal_id}>"


# این خط رو فقط برای تست اولیه می‌زاریم.
# بعد از اینکه app.py رو به‌روز کردی و مطمئن شدی مدل‌ها کار می‌کنن، می‌تونی حذفش کنی.
if __name__ == '__main__':
    with app_test.app_context():
        db.create_all()
        print("جداول دیتابیس (موقت) ساخته شدند.")
