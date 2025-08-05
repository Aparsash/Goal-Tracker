# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from forms import LoginForm, RegistrationForm, GoalForm, UpdateProfileForm, ChangePasswordForm, DeleteAccountForm
from datetime import date, datetime
import os
from models import db, User, Goal, ProgressEntry
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Configuration
import os
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-secret')
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.before_request
def enforce_foreign_keys():
    from sqlalchemy import text
    db.session.execute(text('PRAGMA foreign_keys=ON'))


# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# Login setup
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'لطفاً وارد شوید تا بتوانید به این صفحه دسترسی پیدا کنید.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Authentication
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash('اکانتی با این ایمیل وجود ندارد.', 'error')
        elif user and user.check_password(form.password.data):
            login_user(user)
            flash('با موفقیت وارد شدید.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('رمز عبور اشتباه است.', 'error')

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
            user = User(email=form.email.data, name=form.name.data)
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

# Dashboard
@app.route('/')
@login_required
def index():
    today = date.today().strftime('%Y-%m-%d')
    return render_template('index.html', goals=current_user.goals, today_date=today)

# Goal Management
import jdatetime

@app.route('/add_goal', methods=['GET', 'POST'])
@login_required
def add_goal():
    form = GoalForm()
    if request.method == 'POST':
        # دریافت مقدار تاریخ شمسی به‌صورت رشته
        shamsi_date_str = request.form.get("target_date")
        try:
            year, month, day = map(int, shamsi_date_str.split('-'))
            miladi_date = jdatetime.date(year, month, day).togregorian()
        except:
            flash("تاریخ وارد شده نامعتبر است.", "error")
            return redirect(url_for("add_goal"))

        if form.validate_on_submit():
            goal = Goal(
                title=form.title.data,
                total_units=form.total_units.data,
                daily_target=form.daily_target.data,
                target_date=miladi_date,  # تاریخ به صورت date واقعی
                user_id=current_user.id
            )
            db.session.add(goal)
            db.session.commit()
            flash(f'هدف "{goal.title}" با موفقیت ایجاد شد.', 'success')
            return redirect(url_for('index'))

    return render_template('add_goal.html', form=form)


@app.route('/edit_goal/<int:goal_id>', methods=['GET', 'POST'])
@login_required
def edit_goal(goal_id):
    goal = Goal.query.filter_by(id=goal_id, user_id=current_user.id).first_or_404()
    form = GoalForm(obj=goal)
    if form.validate_on_submit():
        goal.title = form.title.data
        goal.total_units = form.total_units.data
        goal.daily_target = form.daily_target.data
        goal.target_date = form.target_date.data
        db.session.commit()
        flash(f'هدف "{goal.title}" با موفقیت به‌روزرسانی شد.', 'success')
        return redirect(url_for('index'))
    return render_template('edit_goal.html', form=form, goal=goal)

@app.route('/delete_goal/<int:goal_id>', methods=['POST'])
@login_required
def delete_goal(goal_id):
    goal = Goal.query.filter_by(id=goal_id, user_id=current_user.id).first_or_404()
    goal_title = goal.title
    db.session.delete(goal)
    db.session.commit()
    flash(f'هدف "{goal_title}" با موفقیت حذف شد.', 'success')
    return redirect(url_for('index'))

# Progress Submission
@app.route('/submit_progress/<int:goal_id>', methods=['POST'])
@login_required
def submit_progress(goal_id):
    goal = Goal.query.filter_by(id=goal_id, user_id=current_user.id).first_or_404()

    progress_date_str = request.form.get('date')
    progress_value_str = request.form.get('value')

    if not progress_date_str or not progress_value_str:
        flash('لطفاً همه فیلدها را پر کنید.', 'error')
        return redirect(url_for('index'))

    try:
        progress_date = datetime.strptime(progress_date_str, '%Y-%m-%d').date()
        progress_value = float(progress_value_str)

        if progress_value < 0:
            flash('مقدار پیشرفت نمی‌تواند منفی باشد.', 'error')
            return redirect(url_for('index'))

        existing_entry = ProgressEntry.query.filter_by(goal_id=goal.id, date=progress_date).first()
        if existing_entry:
            existing_entry.value = progress_value
            flash(f'پیشرفت برای تاریخ {progress_date_str} آپدیت شد.', 'success')
        else:
            new_entry = ProgressEntry(date=progress_date, value=progress_value, goal_id=goal.id)
            db.session.add(new_entry)
            flash(f'پیشرفت برای تاریخ {progress_date_str} ثبت شد.', 'success')

        db.session.commit()

    except ValueError:
        flash('فرمت تاریخ یا مقدار پیشرفت اشتباه است.', 'error')
    except Exception as e:
        db.session.rollback()
        flash('خطایی در ثبت پیشرفت رخ داده است.', 'error')

    return redirect(url_for('index'))

# Report
@app.route('/report')
@login_required
def report():
    user_goals = current_user.goals

    for goal in user_goals:
        goal.total_progress = sum(entry.value for entry in goal.progress_entries)
        if goal.total_units > 0:
            goal.completion_percentage = min(100, (goal.total_progress / goal.total_units) * 100)
        else:
            goal.completion_percentage = 0
        goal.active_days = len(goal.progress_entries)
        if goal.active_days > 0:
            goal.average_daily_progress = goal.total_progress / goal.active_days
        else:
            goal.average_daily_progress = 0
        if goal.progress_entries:
            goal.last_entry = sorted(goal.progress_entries, key=lambda x: x.date, reverse=True)[0]
        else:
            goal.last_entry = None

    return render_template('report.html', goals=user_goals)

# Profile
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/profile/update', methods=['GET', 'POST'])
@login_required
def update_profile():
    form = UpdateProfileForm(obj=current_user)
    if form.validate_on_submit():
        if form.email.data != current_user.email:
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user:
                flash('این ایمیل قبلاً توسط کاربر دیگری استفاده شده است.', 'error')
                return render_template('update_profile.html', form=form)

        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('اطلاعات حساب شما با موفقیت به‌روزرسانی شد.', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
    return render_template('update_profile.html', form=form)

@app.route('/profile/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('رمز عبور فعلی اشتباه است.', 'error')
        elif form.new_password.data != form.confirm_password.data:
            flash('رمز جدید و تکرار آن مطابقت ندارند.', 'error')
        else:
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('رمز عبور شما با موفقیت تغییر کرد.', 'success')
            return redirect(url_for('profile'))
    return render_template('change_password.html', form=form)


@app.route('/profile/delete')
@login_required
def delete_account():
    return render_template('delete_account.html')

@app.route('/confirm_delete', methods=['POST'])
@login_required
def confirm_delete():
    user_id = current_user.id
    username = current_user.name or current_user.email
    logout_user()
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return jsonify({'message': f'حساب کاربری {username} حذف شد.'}), 200

if __name__ == '__main__':
    app.run(debug=True)