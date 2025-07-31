# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
# اضافه کردن واردات‌های جدید
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
# برای کار با تاریخ
from datetime import datetime
import os

app = Flask(__name__)

# === تنظیمات امنیت و دیتابیس ===
# یه کلید مخفی برای امنیت sessionها. حتماً تو محیط واقعی این رو عوض کن!
# می‌تونی از python -c "import secrets; print(secrets.token_hex(16))" یه کلید امن بسازی
app.config['SECRET_KEY'] = '30662e4a93fe55b325d02a0b0b3cd0ac' 
# مسیر فایل دیتابیس SQLite. اگه نباشه، خودش می‌سازه.
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "site.db")}'
# برای جلوگیری از یه اخطار
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# === راه‌اندازی ابزارها ===
db = SQLAlchemy(app)
login_manager = LoginManager(app)
# اگه کاربر لاگین نکرده و سعی کنه بره صفحه‌ای که نیاز به لاگین داره، به /login هدایتش کن.
login_manager.login_view = 'login'
login_manager.login_message = 'لطفاً وارد شوید تا بتوانید به این صفحه دسترسی پیدا کنید.'

# === تابع مورد نیاز برای Flask-Login ===
# این تابع باید یه کاربر رو بر اساس id پیدا کنه.
# ما مدل User رو تو models.py تعریف کردیم.
# اول باید models.py رو ایمپورت کنیم تا کلاس User تعریف بشه.
from models import User, Goal, ProgressEntry

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# === routeهای اصلی (با محافظت لاگین) ===

@app.route('/')
@login_required
def index():
    # فقط اهداف کاربر فعلی رو نشون بده
    user_goals = current_user.goals
    return render_template('index.html', goals=user_goals)

@app.route('/report')
@login_required
def report():
    # فقط گزارش اهداف کاربر فعلی رو نشون بده
    user_goals = current_user.goals
    return render_template('report.html', goals=user_goals)

# === routeهای جدید برای لاگین/ثبت‌نام (موقت خالی) ===
# اینا رو تو مراحل بعدی پر می‌کنیم.

@app.route('/login', methods=['GET', 'POST'])
def login():
    return "صفحه لاگین - در آینده پر می‌شه"

@app.route('/register', methods=['GET', 'POST'])
def register():
    return "صفحه ثبت‌نام - در آینده پر می‌شه"

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# === route برای ثبت پیشرفت (موقت) ===
@app.route('/submit', methods=['POST'])
@login_required
def submit():
    # این یه راه حل موقت هست. بعداً پر می‌شه.
    # اینجا باید داده‌های فرم رو بگیریم و تو دیتابیس ذخیره کنیم.
    flash("پیشرفت ثبت شد (موقت)", "success")
    return redirect(url_for('index'))

# === ساخت جداول دیتابیس ===
# این خط رو به app context محدود می‌کنیم.
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
