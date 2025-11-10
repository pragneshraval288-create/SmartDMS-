from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, Optional

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

    submit = SubmitField("Update Profile")
