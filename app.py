# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
# Import form classes
from forms import LoginForm, RegistrationForm, GoalForm
# For working with dates
from datetime import date, datetime
import os

from models import db, User, Goal, ProgressEntry

app = Flask(__name__)

# Secret key for security (change this in production!)
app.config['SECRET_KEY'] = '30662e4a93fe55b325d02a0b0b3cd0ac'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "site.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Initialize login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'لطفاً وارد شوید تا بتوانید به این صفحه دسترسی پیدا کنید.'

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))

# === Authentication Routes ===

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
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
    """User registration route"""
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
    """User logout route"""
    logout_user()
    return redirect(url_for('login'))

# === Main Application Routes ===

@app.route('/')
@login_required
def index():
    """Main dashboard - shows user's goals and progress form"""
    # Send today's date to template for default value in form
    today = date.today().strftime('%Y-%m-%d')
    return render_template('index.html', goals=current_user.goals, today_date=today)

# === Goal Management Routes ===

@app.route('/add_goal', methods=['GET', 'POST'])
@login_required
def add_goal():
    """Add a new goal for the current user"""
    form = GoalForm()
    if form.validate_on_submit():
        # Create new goal
        goal = Goal(
            title=form.title.data,
            total_units=form.total_units.data,
            daily_target=form.daily_target.data,
            target_date=form.target_date.data,
            user_id=current_user.id  # Ownership for current user
        )
        db.session.add(goal)
        db.session.commit()
        flash(f'هدف "{goal.title}" با موفقیت ایجاد شد.', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_goal.html', form=form)

@app.route('/edit_goal/<int:goal_id>', methods=['GET', 'POST'])
@login_required
def edit_goal(goal_id):
    """Edit an existing goal (only if owned by current user)"""
    goal = Goal.query.filter_by(id=goal_id, user_id=current_user.id).first_or_404()
    form = GoalForm(obj=goal) # Populate form with current goal data
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
    """Delete a goal (only if owned by current user)"""
    goal = Goal.query.filter_by(id=goal_id, user_id=current_user.id).first_or_404()
    goal_title = goal.title
    db.session.delete(goal)
    db.session.commit()
    flash(f'هدف "{goal_title}" با موفقیت حذف شد.', 'success')
    return redirect(url_for('index'))

# === Progress Reporting Route ===

@app.route('/report')
@login_required
def report():
    """Generate personalized progress report for current user"""
    user_goals = current_user.goals
    
    # Calculate statistics for each goal
    for goal in user_goals:
        # Total progress
        goal.total_progress = sum(entry.value for entry in goal.progress_entries)
        # Completion percentage
        if goal.total_units > 0:
            goal.completion_percentage = min(100, (goal.total_progress / goal.total_units) * 100)
        else:
            goal.completion_percentage = 0
        # Active days (days with progress recorded)
        goal.active_days = len(goal.progress_entries)
        # Average daily progress
        if goal.active_days > 0:
            goal.average_daily_progress = goal.total_progress / goal.active_days
        else:
            goal.average_daily_progress = 0
            
        # Last entry
        if goal.progress_entries:
            goal.last_entry = sorted(goal.progress_entries, key=lambda x: x.date, reverse=True)[0]
        else:
            goal.last_entry = None

    return render_template('report.html', goals=user_goals)

# === Daily Progress Submission Route ===

@app.route('/submit_progress/<int:goal_id>', methods=['POST'])
@login_required
def submit_progress(goal_id):
    """Submit daily progress for a specific goal"""
    # Check if goal belongs to current user
    goal = Goal.query.filter_by(id=goal_id, user_id=current_user.id).first_or_404()
    
    # Get data from form
    progress_date_str = request.form.get('date')
    progress_value_str = request.form.get('value')
    
    if not progress_date_str or not progress_value_str:
        flash('لطفاً همه فیلدها را پر کنید.', 'error')
        return redirect(url_for('index'))
    
    try:
        # Convert date and value
        progress_date = datetime.strptime(progress_date_str, '%Y-%m-%d').date()
        progress_value = float(progress_value_str)
        
        if progress_value < 0:
            flash('مقدار پیشرفت نمی‌تواند منفی باشد.', 'error')
            return redirect(url_for('index'))
        
        # Check if progress already exists for this date
        existing_entry = ProgressEntry.query.filter_by(goal_id=goal.id, date=progress_date).first()
        if existing_entry:
            # Update existing entry
            existing_entry.value = progress_value
            flash(f'پیشرفت برای تاریخ {progress_date_str} آپدیت شد.', 'success')
        else:
            # Create new entry
            new_entry = ProgressEntry(date=progress_date, value=progress_value, goal_id=goal.id)
            db.session.add(new_entry)
            flash(f'پیشرفت برای تاریخ {progress_date_str} ثبت شد.', 'success')
        
        db.session.commit()
        
    except ValueError:
        flash('فرمت تاریخ یا مقدار پیشرفت اشتباه است.', 'error')
    except Exception as e:
        db.session.rollback()
        flash('خطایی در ثبت پیشرفت رخ داده است.', 'error')
        # You can log this error for debugging
    
    return redirect(url_for('index'))


# === Create database tables ===
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
