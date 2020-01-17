from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateTimeField, SelectField
from wtforms.validators import ValidationError, Email, EqualTo
from wtforms.validators import DataRequired
from app.models import Patient


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    firstname = StringField('Firstname', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        patient = Patient.query.filter_by(login=email.data).first()
        if patient is not None:
            raise ValidationError('Please use a different email.')

class VisitingForm(FlaskForm):
    region = SelectField("Region", choices=[])
    branch = SelectField("Branch", choices=[])
    doctor = SelectField("Doctor", choices=[])
    date = DateTimeField("Date", format='%Y-%m-%d %h:%m:%s')
    submit = SubmitField("Submit")

class IndexForm(FlaskForm):
    region = SelectField("Region", choices=[])
    branch = SelectField("Branch", choices=[])
    doctor = SelectField("Doctor", choices=[])

