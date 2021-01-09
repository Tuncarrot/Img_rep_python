from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, MultipleFileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from imgRepFlask.models import User, Account, ContactInfo, Album, Picture

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        email = Account.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email is already registered, please choose another email')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def validate_email(self, email):
        #if email.data != current_user.email:
        user = Account.query.filter_by(id=current_user.id).first()
        if email.data != user.email:
            email = Account.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('Email is already registered, please choose another email')

class UploadPhotoForm(FlaskForm):
    name = StringField('Title', validators=[DataRequired(), Length(min=2, max=30)])
    date = StringField('Date', validators=[Length(min=8, max=10)])
    image_file = MultipleFileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Upload')
