from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(3,150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(3,150)])
    submit   = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(3,150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(3,150)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('user','User'),('admin','Admin')])
    submit = SubmitField('Register')

class ResetPasswordForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(3,150)])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(3,150)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Reset Password')
