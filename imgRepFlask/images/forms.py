from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, MultipleFileField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from flask_wtf.file import FileField, FileAllowed

class UploadPhotoForm(FlaskForm):
    name = StringField('Title', validators=[DataRequired(), Length(min=2, max=30)])
    image_file = MultipleFileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Upload')