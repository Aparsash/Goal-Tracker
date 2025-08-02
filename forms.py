from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, NumberRange
from datetime import date

class LoginForm(FlaskForm):
    email = StringField('ایمیل', validators=[DataRequired(), Email()], render_kw={"placeholder": "example@email.com"})
    password = PasswordField('رمز عبور', validators=[DataRequired()], render_kw={"placeholder": "رمز عبور خود را وارد کنید"})
    submit = SubmitField('ورود')

class RegistrationForm(FlaskForm):
    name = StringField('نام کامل', validators=[Length(max=100)], render_kw={"placeholder": "نام و نام خانوادگی"})
    email = StringField('ایمیل', validators=[DataRequired(), Email(), Length(max=120)], render_kw={"placeholder": "ایمیل خود را وارد کنید"})
    password = PasswordField('رمز عبور', validators=[
        DataRequired(),
        Length(min=6),
        Regexp(r'^(?=.*[A-Za-z])(?=.*\\d)', message="رمز عبور باید شامل حروف و عدد باشد.")
    ], render_kw={"placeholder": "رمز عبور قوی وارد کنید"})
    password2 = PasswordField('تکرار رمز عبور', validators=[
        DataRequired(),
        EqualTo('password', message='رمز عبور مطابقت ندارد.')
    ], render_kw={"placeholder": "دوباره رمز عبور را وارد کنید"})
    submit = SubmitField('ثبت‌نام')

class GoalForm(FlaskForm):
    title = StringField('عنوان هدف', validators=[DataRequired()], render_kw={"placeholder": "یادگیری پایتون"})
    total_units = FloatField('تعداد کل واحدها', validators=[DataRequired(), NumberRange(min=0.1)], render_kw={"placeholder": "مثلاً: 50"})
    daily_target = FloatField('هدف روزانه', validators=[DataRequired(), NumberRange(min=0.01)], render_kw={"placeholder": "مثلاً: 1"})
    target_date = DateField('تاریخ پایان', validators=[DataRequired()], default=date.today, format='%Y-%m-%d')
    submit = SubmitField('ایجاد هدف')

class UpdateProfileForm(FlaskForm):
    name = StringField('نام کامل', validators=[Length(max=100)], render_kw={"placeholder": "نام جدید"})
    email = StringField('ایمیل', validators=[DataRequired(), Email(), Length(max=120)], render_kw={"placeholder": "ایمیل جدید"})
    submit = SubmitField('به‌روزرسانی اطلاعات')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('رمز عبور فعلی', validators=[DataRequired()], render_kw={"placeholder": "رمز فعلی"})
    new_password = PasswordField('رمز عبور جدید', validators=[
        DataRequired(),
        Length(min=6),
        Regexp(r'^(?=.*[A-Za-z])(?=.*\\d)', message="رمز باید شامل حروف و عدد باشد.")
    ], render_kw={"placeholder": "رمز جدید"})
    new_password2 = PasswordField('تکرار رمز جدید', validators=[
        DataRequired(),
        EqualTo('new_password', message='رمزها مطابقت ندارند.')
    ], render_kw={"placeholder": "تکرار رمز جدید"})
    submit = SubmitField('تغییر رمز عبور')

class DeleteAccountForm(FlaskForm):
    confirm = StringField('تایید حذف', validators=[DataRequired(), EqualTo('confirm', message="عبارت را دقیق وارد کنید.")], render_kw={"placeholder": "حذف حساب"})
    submit = SubmitField('حذف حساب')
