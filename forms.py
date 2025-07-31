# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp

class LoginForm(FlaskForm):
    """فرم ورود کاربر"""
    email = StringField('ایمیل', validators=[DataRequired(), Email()], render_kw={"placeholder": "example@email.com"})
    password = PasswordField('رمز عبور', validators=[DataRequired()], render_kw={"placeholder": "رمز عبور خود را وارد کنید"})
    submit = SubmitField('ورود')

class RegistrationForm(FlaskForm):
    """فرم ثبت‌نام کاربر"""
    email = StringField('ایمیل', validators=[DataRequired(), Email(), Length(max=120)], render_kw={"placeholder": "example@email.com"})
    # تغییر اعتبارسنجی رمز عبور برای اجبار به حروف و اعداد
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
