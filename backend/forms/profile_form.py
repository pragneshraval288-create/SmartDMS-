from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, Regexp, Optional, EqualTo

phone_regex = r'^\+?\d{10,15}$'

class ProfileForm(FlaskForm):
    full_name = StringField("Full Name", validators=[
        DataRequired(), Length(min=2, max=150)
    ])

    email = StringField("Email", validators=[
        DataRequired(), Email(), Length(max=150)
    ])

    mobile = StringField("Mobile Number", validators=[
        Optional(), Regexp(phone_regex, message="Invalid mobile number")
    ])

    dob = DateField("Date of Birth", format='%Y-%m-%d', validators=[
        Optional()
    ])

    # Profile picture is uploaded via <input type="file"> in template (handled in route)
    # For password change:
    current_password = PasswordField("Current Password (required to change email/mobile/password)", validators=[
        Optional(), Length(min=3, max=150)
    ])

    new_password = PasswordField("New Password", validators=[
        Optional(), Length(min=6, max=150)
    ])
    confirm_password = PasswordField("Confirm New Password", validators=[
        Optional(), EqualTo("new_password", message="Passwords must match")
    ])

    submit = SubmitField("Save Changes")
