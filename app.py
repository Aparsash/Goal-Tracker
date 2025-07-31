# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
# اضافه کردن واردات فرم‌های جدید
from forms import LoginForm, RegistrationForm, GoalForm
# برای کار با تاریخ
from datetime import date, datetime
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
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('با موفقیت وارد شدید.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('ایمیل یا رمز عبور اشتباه است.', 'error')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('این ایمیل قبلاً ثبت‌نام کرده است.', 'error')
        else:
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
    # ارسال تاریخ امروز به تمپلیت برای پیش‌فرض قرار دادن در فرم
    today = date.today().strftime('%Y-%m-%d')
    return render_template('index.html', goals=current_user.goals, today_date=today)

# === route جدید برای ایجاد هدف ===
@app.route('/add_goal', methods=['GET', 'POST'])
@login_required
def add_goal():
    form = GoalForm()
    if form.validate_on_submit():
        # ساخت هدف جدید
        goal = Goal(
            title=form.title.data,
            total_units=form.total_units.data,
            daily_target=form.daily_target.data,
            target_date=form.target_date.data,
            user_id=current_user.id  # مالکیت هدف برای کاربر فعلی
        )
        db.session.add(goal)
        db.session.commit()
        flash(f'هدف "{goal.title}" با موفقیت ایجاد شد.', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_goal.html', form=form)

# === route جدید برای مشاهده گزارش ===
@app.route('/report')
@login_required
def report():
    user_goals = current_user.goals
    
    # محاسبه آمار برای هر هدف
    for goal in user_goals:
        # کل پیشرفت
        goal.total_progress = sum(entry.value for entry in goal.progress_entries)
        # درصد تکمیل
        if goal.total_units > 0:
            goal.completion_percentage = min(100, (goal.total_progress / goal.total_units) * 100)
        else:
            goal.completion_percentage = 0
        # تعداد روزهای فعال (روزهایی که پیشرفت ثبت شده)
        goal.active_days = len(goal.progress_entries)
        # میانگین پیشرفت روزانه
        if goal.active_days > 0:
            goal.average_daily_progress = goal.total_progress / goal.active_days
        else:
            goal.average_daily_progress = 0
            
        # آخرین پیشرفت
        if goal.progress_entries:
            goal.last_entry = sorted(goal.progress_entries, key=lambda x: x.date, reverse=True)[0]
        else:
            goal.last_entry = None

    return render_template('report.html', goals=user_goals)

# === route جدید برای ثبت پیشرفت ===
@app.route('/submit_progress/<int:goal_id>', methods=['POST'])
@login_required
def submit_progress(goal_id):
    # چک کردن اینکه هدف متعلق به کاربر فعلی هست یا نه
    goal = Goal.query.filter_by(id=goal_id, user_id=current_user.id).first_or_404()
    
    # دریافت داده‌ها از فرم
    progress_date_str = request.form.get('date')
    progress_value_str = request.form.get('value')
    
    if not progress_date_str or not progress_value_str:
        flash('لطفاً همه فیلدها را پر کنید.', 'error')
        return redirect(url_for('index'))
    
    try:
        # تبدیل تاریخ و مقدار
        progress_date = datetime.strptime(progress_date_str, '%Y-%m-%d').date()
        progress_value = float(progress_value_str)
        
        if progress_value < 0:
            flash('مقدار پیشرفت نمی‌تواند منفی باشد.', 'error')
            return redirect(url_for('index'))
        
        # چک کردن اینکه آیا قبلاً برای این تاریخ پیشرفت ثبت شده یا نه
        existing_entry = ProgressEntry.query.filter_by(goal_id=goal.id, date=progress_date).first()
        if existing_entry:
            # اگه قبلاً ثبت شده، مقدار رو آپدیت کن
            existing_entry.value = progress_value
            flash(f'پیشرفت برای تاریخ {progress_date_str} آپدیت شد.', 'success')
        else:
            # اگه قبلاً ثبت نشده، یه رکورد جدید بساز
            new_entry = ProgressEntry(date=progress_date, value=progress_value, goal_id=goal.id)
            db.session.add(new_entry)
            flash(f'پیشرفت برای تاریخ {progress_date_str} ثبت شد.', 'success')
        
        db.session.commit()
        
    except ValueError:
        flash('فرمت تاریخ یا مقدار پیشرفت اشتباه است.', 'error')
    except Exception as e:
        db.session.rollback()
        flash('خطایی در ثبت پیشرفت رخ داده است.', 'error')
        # می‌تونی این خطا رو لاگ کنی برای دیباگ بیشتر
    
    return redirect(url_for('index'))


# === ساخت جداول دیتابیس ===
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
