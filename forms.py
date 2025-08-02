# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
import re
from wtforms.fields import StringField

class RegistrationForm(FlaskForm):
    name = StringField('نام', validators=[DataRequired(), Length(min=2, max=100)],
        render_kw={"placeholder": "مثلاً: پارسا"}
    )
    email = StringField('ایمیل', validators=[DataRequired(), Email()],
        render_kw={"placeholder": "مثلاً: you@example.com"}
    )
    password = PasswordField('رمز عبور', validators=[DataRequired(), Length(min=8)],
        render_kw={"placeholder": "مثلاً: MySecurePass123"},
        description="باید حداقل ۸ کاراکتر، شامل حروف و اعداد باشد."
    )
    confirm_password = PasswordField('تکرار رمز عبور', validators=[DataRequired(), EqualTo('password')],
        render_kw={"placeholder": "رمز عبور را دوباره وارد کنید"}
    )
    submit = SubmitField('ثبت نام')

    def validate_password(self, field):
        password = field.data
        if not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
            raise ValidationError("رمز عبور باید شامل حروف و عدد باشد.")

class LoginForm(FlaskForm):
    email = StringField('ایمیل', validators=[DataRequired(), Email()],
        render_kw={"placeholder": "مثلاً: you@example.com"})
    password = PasswordField('رمز عبور', validators=[DataRequired()],
        render_kw={"placeholder": "رمز عبور خود را وارد کنید"})
    submit = SubmitField('ورود')

class GoalForm(FlaskForm):
    title = StringField('عنوان هدف', validators=[DataRequired()],
        render_kw={"placeholder": "مثلاً: مطالعه روزانه"})
    total_units = FloatField('تعداد کل واحدها', validators=[DataRequired()],
        render_kw={"placeholder": "مثلاً: 100"})
    daily_target = FloatField('هدف روزانه', validators=[DataRequired()],
        render_kw={"placeholder": "مثلاً: 5"})
    target_date = DateField("تاریخ هدف نهایی", format="%Y-%m-%d",
        render_kw={"type": "date"})  # HTML5 native date picker

    submit = SubmitField('ثبت هدف')

class UpdateProfileForm(FlaskForm):
    name = StringField('نام', validators=[DataRequired(), Length(min=2, max=100)],
        render_kw={"placeholder": "مثلاً: پارسا"})
    email = StringField('ایمیل', validators=[DataRequired(), Email()],
        render_kw={"placeholder": "مثلاً: you@example.com"})
    submit = SubmitField('به‌روزرسانی')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('رمز عبور فعلی', validators=[DataRequired()],
        render_kw={"placeholder": "رمز فعلی خود را وارد کنید"})
    new_password = PasswordField('رمز عبور جدید', validators=[DataRequired(), Length(min=8)],
        render_kw={"placeholder": "مثلاً: newpass123"},
        description="رمز جدید باید حداقل ۸ کاراکتر، شامل حرف و عدد باشد.")
    confirm_password = PasswordField('تکرار رمز جدید', validators=[DataRequired(), EqualTo('new_password', message='رمز جدید و تکرار آن باید یکسان باشند.')],
        render_kw={"placeholder": "رمز جدید را دوباره وارد کنید"})
    submit = SubmitField('تغییر رمز')



class DeleteAccountForm(FlaskForm):
    confirm = StringField('تأیید حذف', validators=[DataRequired()],
        render_kw={"placeholder": "حذف حساب"})
    submit = SubmitField('حذف حساب کاربری') 