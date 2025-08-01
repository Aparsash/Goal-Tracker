# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, NumberRange
from datetime import date

class LoginForm(FlaskForm):
    """فرم ورود کاربر"""
    email = StringField('ایمیل', validators=[DataRequired(), Email()], render_kw={"placeholder": "example@email.com"})
    password = PasswordField('رمز عبور', validators=[DataRequired()], render_kw={"placeholder": "رمز عبور خود را وارد کنید"})
    submit = SubmitField('ورود')

class RegistrationForm(FlaskForm):
    """فرم ثبت‌نام کاربر"""
    email = StringField('ایمیل', validators=[DataRequired(), Email(), Length(max=120)], render_kw={"placeholder": "example@email.com"})
    password = PasswordField('رمز عبور', validators=[
        DataRequired(), 
        Length(min=6),
        Regexp(r'^(?=.*[A-Za-z])(?=.*\d)', message="رمز عبور باید شامل حروف و اعداد باشد.")
    ], render_kw={"placeholder": "حداقل 6 کاراکتر، شامل حروف و اعداد"})
    password2 = PasswordField(
        'تکرار رمز عبور', 
        validators=[
            DataRequired(), 
            EqualTo('password', message='رمزهای عبور مطابقت ندارند.')
        ],
        render_kw={"placeholder": "رمز عبور خود را دوباره وارد کنید"}
    )
    submit = SubmitField('ثبت‌نام')

# === Form for creating/editing goals ===
class GoalForm(FlaskForm):
    """Form for creating or editing a goal"""
    title = StringField('عنوان هدف', validators=[DataRequired()], render_kw={"placeholder": "مثلاً: یادگیری پایتون"})
    total_units = FloatField('تعداد کل واحدها', validators=[DataRequired(), NumberRange(min=0.1, message="تعداد کل واحدها باید بیشتر از صفر باشد.")], render_kw={"placeholder": "مثلاً: 50"})
    daily_target = FloatField('مقدار هدف روزانه', validators=[DataRequired(), NumberRange(min=0.01, message="مقدار هدف روزانه باید بیشتر از صفر باشد.")], render_kw={"placeholder": "مثلاً: 1"})
    target_date = DateField('تاریخ پایان هدف', validators=[DataRequired()], default=date.today, format='%Y-%m-%d')
    submit = SubmitField('ایجاد هدف')
