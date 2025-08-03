from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, NumberRange
import re

# Registration form with validation
class RegistrationForm(FlaskForm):
    name = StringField('نام', validators=[
        DataRequired(message="نام نمی‌تواند خالی باشد."),
        Length(min=2, max=100, message="نام باید حداقل ۲ و حداکثر ۱۰۰ کاراکتر باشد.")
    ], render_kw={"placeholder": "مثلاً: پارسا"})

    email = StringField('ایمیل', validators=[
        DataRequired(message="ایمیل الزامی است."),
        Email(message="لطفاً یک ایمیل معتبر وارد کنید.")
    ], render_kw={"placeholder": "مثلاً: you@example.com"})

    password = PasswordField('رمز عبور', validators=[
        DataRequired(message="رمز عبور الزامی است.")
        # ⛔ intentionally NOT adding Length here to avoid minlength HTML attribute
    ], render_kw={"placeholder": "مثلاً: MySecurePass123"},
       description="باید حداقل ۸ کاراکتر، شامل حروف و اعداد باشد.")

    confirm_password = PasswordField('تکرار رمز عبور', validators=[
        DataRequired(message="تأیید رمز عبور الزامی است."),
        EqualTo('password', message="رمز عبور و تکرار آن باید یکسان باشند.")
    ], render_kw={"placeholder": "رمز عبور را دوباره وارد کنید"})

    submit = SubmitField('ثبت نام')

    def validate_password(self, field):
        password = field.data

        # ✅ Custom server-side validation only
        if len(password) < 8:
            raise ValidationError("رمز عبور باید حداقل ۸ کاراکتر باشد.")
        if not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
            raise ValidationError("رمز عبور باید شامل حروف و عدد باشد.")


# Login form with email/password validation
class LoginForm(FlaskForm):
    email = StringField('ایمیل', validators=[
        DataRequired(message="ایمیل الزامی است."),
        Email(message="لطفاً یک ایمیل معتبر وارد کنید.")
    ], render_kw={"placeholder": "مثلاً: you@example.com"})

    password = PasswordField('رمز عبور', validators=[
        DataRequired(message="رمز عبور الزامی است.")
    ], render_kw={"placeholder": "رمز عبور خود را وارد کنید"})

    submit = SubmitField('ورود')

# Goal form used for both adding and editing goals
class GoalForm(FlaskForm):
    title = StringField('عنوان هدف', validators=[
        DataRequired(message="عنوان هدف نمی‌تواند خالی باشد.")
    ], render_kw={"placeholder": "مثلاً: مطالعه روزانه"})

    total_units = FloatField('تعداد کل واحدها', validators=[
        DataRequired(message="تعداد کل واحدها الزامی است."),
        NumberRange(min=0.01, message="مقدار باید یک عدد مثبت باشد.")
    ], render_kw={"placeholder": "مثلاً: 100"})

    daily_target = FloatField('هدف روزانه', validators=[
        DataRequired(message="هدف روزانه الزامی است."),
        NumberRange(min=0.01, message="هدف روزانه باید یک عدد مثبت باشد.")
    ], render_kw={"placeholder": "مثلاً: 5"})

    target_date = DateField("تاریخ هدف نهایی", format="%Y-%m-%d",
        render_kw={"type": "date"})

    submit = SubmitField('ثبت هدف')

# Profile update form
class UpdateProfileForm(FlaskForm):
    name = StringField('نام', validators=[
        DataRequired(message="نام الزامی است."),
        Length(min=2, max=100, message="نام باید بین ۲ تا ۱۰۰ کاراکتر باشد.")
    ], render_kw={"placeholder": "مثلاً: پارسا"})

    email = StringField('ایمیل', validators=[
        DataRequired(message="ایمیل الزامی است."),
        Email(message="لطفاً یک ایمیل معتبر وارد کنید.")
    ], render_kw={"placeholder": "مثلاً: you@example.com"})

    submit = SubmitField('به‌روزرسانی')

# Password change form with validation
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('رمز عبور فعلی', validators=[
        DataRequired(message="رمز فعلی الزامی است.")
    ], render_kw={"placeholder": "رمز فعلی خود را وارد کنید"})

    new_password = PasswordField('رمز عبور جدید', validators=[
        DataRequired(message="رمز جدید الزامی است."),
        Length(min=8, message="رمز جدید باید حداقل ۸ کاراکتر باشد.")
    ], render_kw={"placeholder": "مثلاً: newpass123"},
       description="رمز جدید باید حداقل ۸ کاراکتر، شامل حرف و عدد باشد.")

    confirm_password = PasswordField('تکرار رمز جدید', validators=[
        DataRequired(message="تأیید رمز جدید الزامی است."),
        EqualTo('new_password', message="رمز جدید و تکرار آن باید یکسان باشند.")
    ], render_kw={"placeholder": "رمز جدید را دوباره وارد کنید"})

    submit = SubmitField('تغییر رمز')

# Confirm delete account form
class DeleteAccountForm(FlaskForm):
    confirm = StringField('تأیید حذف', validators=[
        DataRequired(message="برای حذف حساب، این فیلد باید پر شود.")
    ], render_kw={"placeholder": "حذف حساب"})

    submit = SubmitField('حذف حساب کاربری')
