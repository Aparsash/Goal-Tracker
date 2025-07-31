# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
# اضافه کردن واردات فرم‌ها
from forms import LoginForm, RegistrationForm
import os

from models import db, User, Goal, ProgressEntry

app = Flask(__name__)

app.config['SECRET_KEY'] = '30662e4a93fe55b325d02a0b0b3cd0ac'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "site.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'لطفاً وارد شوید تا بتوانید به این صفحه دسترسی پیدا کنید.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# === routeهای احراز هویت ===

@app.route('/login', methods=['GET', 'POST'])
def login():
    # اگه کاربر قبلاً لاگین کرده، به صفحه اصلی بره
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('با موفقیت وارد شدید.', 'success')
            # اگه کاربر از صفحه‌ای دیگه اومده بود که نیاز به لاگین داشت، به اون صفحه برگرده
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('ایمیل یا رمز عبور اشتباه است.', 'error')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    # اگه کاربر قبلاً لاگین کرده، به صفحه اصلی بره
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # چک کردن تکراری نبودن ایمیل
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('این ایمیل قبلاً ثبت‌نام کرده است.', 'error')
        else:
            # ساخت کاربر جدید
            user = User(email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('ثبت‌نام با موفقیت انجام شد. لطفاً وارد شوید.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# === routeهای اصلی ===

@app.route('/')
@login_required
def index():
    return render_template('index.html', goals=current_user.goals)

@app.route('/report')
@login_required
def report():
    return render_template('report.html', goals=current_user.goals)

# === ساخت جداول دیتابیس ===
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
