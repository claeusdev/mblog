from wtforms.validators import DataRequired, EqualTo, Email, Length
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,TextAreaField, BooleanField, SubmitField, ValidationError

from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    '''removing email validator now for later.'''
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign Up")


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Username already taken.")


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different username")

class EditProfileForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    about_me = TextAreaField("About me", validators=[Length(min=0,max=256)])
    submit = SubmitField("Update profile")

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError("Username already taken")
