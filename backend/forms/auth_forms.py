from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField,
    SelectField, DateField
)
from wtforms.validators import (
    DataRequired, Length, EqualTo, Email,
    Regexp, Optional, ValidationError
)
from backend.models.models import User


# ✅ Mobile validation regex (10–15 digit)
phone_regex = r'^\+?\d{10,15}$'


# ✅✅ LOGIN FORM
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), Length(3,150)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(3,150)
    ])
    submit   = SubmitField('Login')



# ✅✅ REGISTER FORM (FULL DETAILS)
class RegisterForm(FlaskForm):

    full_name = StringField('Full Name', validators=[
        DataRequired(), Length(min=2, max=150)
    ])

    email = StringField('Email', validators=[
        DataRequired(), Email(), Length(max=150)
    ])

    mobile = StringField('Mobile Number', validators=[
        Optional(), Regexp(phone_regex, message="Invalid mobile number")
    ])

    dob = DateField('Date of Birth (YYYY-MM-DD)', format='%Y-%m-%d', validators=[
        Optional()
    ])

    username = StringField('Username', validators=[
        DataRequired(), Length(3,150)
    ])

    password = PasswordField('Password', validators=[
        DataRequired(), Length(3,150)
    ])

    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password')
    ])

    role = SelectField('Role', choices=[
        ('user', 'User'),
        ('admin', 'Admin')
    ])

    submit = SubmitField('Register')

    # ✅ Username must be unique
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already taken.")

    # ✅ Email must be unique
    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError("Email already registered.")

    # ✅ Mobile must be unique (if provided)
    def validate_mobile(self, field):
        if field.data:
            if User.query.filter_by(mobile=field.data).first():
                raise ValidationError("Mobile number already used.")



# ✅✅ RESET PASSWORD FORM (USERNAME + EMAIL + MOBILE REQUIRED)
class ResetPasswordForm(FlaskForm):

    username = StringField('Username', validators=[
        DataRequired(), Length(3,150)
    ])

    email = StringField('Email', validators=[
        DataRequired(), Email(), Length(max=150)
    ])

    mobile = StringField('Mobile Number', validators=[
        DataRequired(), Regexp(phone_regex, message="Invalid mobile number")
    ])

    new_password = PasswordField('New Password', validators=[
        DataRequired(), Length(3,150)
    ])

    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('new_password')
    ])

    submit = SubmitField('Reset Password')
