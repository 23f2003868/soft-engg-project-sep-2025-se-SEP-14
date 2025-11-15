
from flask_wtf import FlaskForm
from wtforms import DateTimeField, FloatField, StringField, PasswordField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired,EqualTo
from wtforms.validators import optional,Email,Length,Optional
from flask_wtf.file import FileField, FileAllowed

class RegisterAdminForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register/Update')

class RegisterRecruiterForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    company = StringField('Company', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    linkdin_profile_path = StringField('Linkdin', validators=[DataRequired()])
    submit = SubmitField('Register/Update')


class RegisterCandidateForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    education = SelectField('Education', validators=[DataRequired()])  # Assume choices are set somewhere else
    age = StringField('Age', validators=[DataRequired()])
    file = FileField('Resume', validators=[optional(), FileAllowed(['pdf'])])
    submit = SubmitField('Register/Update')


class CreateJobForm(FlaskForm):
    job_title = StringField('Job Title', validators=[DataRequired()])
    location = IntegerField('Location', validators=[DataRequired()])
    job_type = IntegerField('Job type', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Register/Update')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password', message='Passwords must match')])
    submit = SubmitField('Change Password')


class LoginForm(FlaskForm):
    email = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

