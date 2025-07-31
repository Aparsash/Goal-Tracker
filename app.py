# app.py
from flask import Flask, render_template, request, redirect, url_for
# اضافه کردن واردات‌های جدید
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
# برای هش کردن رمز عبور
from werkzeug.security import generate_password_hash, check_password_hash
# برای کار با تاریخ
from datetime import datetime
import os

app = Flask(__name__)

# === تنظیمات امنیت و دیتابیس ===
# یه کلید مخفی برای امنیت sessionها. حتماً تو محیط واقعی این رو عوض کن!
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
# ما بعداً مدل User رو تعریف می‌کنیم.
from models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# === مدل‌ها ===
# مدل‌ها رو تو یه فایل جدا تعریف می‌کنیم (models.py).
# اینجا فقط اشاره می‌کنیم که وجود دارن.

# === routeهای فعلی (موقت) ===
# برای تست اولیه، routeهای قبلی رو نگه می‌داریم، ولی بعداً تغییر می‌دن.
# برای اینکه بدون لاگین نره، یه شرط ساده می‌زاریم.

@app.route('/')
def index():
    # این یه راه حل موقت هست. بعداً با @login_required جایگزین می‌شه.
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    # اینجا باید اهداف کاربر فعلی نمایش داده بشن. فعلاً یه لیست خالی.
    return render_template('index.html', goals=[])

@app.route('/report')
def report():
    # این یه راه حل موقت هست. بعداً با @login_required جایگزین می‌شه.
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    # اینجا باید گزارش کاربر فعلی نمایش داده بشن. فعلاً یه لیست خالی.
    return render_template('report.html', goals=[])

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

# این routeهای قبلی‌ات رو هم نگه می‌داریم ولی بعداً تغییر می‌کنن.
@app.route('/submit', methods=['POST'])
def submit():
    # این یه راه حل موقت هست.
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return "پیشرفت ثبت شد (موقت)"

if __name__ == '__main__':
    # این خط مهمه: اولین بار که برنامه اجرا می‌شه، جداول دیتابیس رو می‌سازه.
    with app.app_context():
        db.create_all()
    app.run(debug=True)
