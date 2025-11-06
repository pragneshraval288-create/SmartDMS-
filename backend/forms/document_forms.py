from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired

class DocumentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    tags  = StringField('Tags')
    file  = FileField('File')
    submit = SubmitField('Submit')
