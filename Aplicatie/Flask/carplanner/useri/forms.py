# Form Based Imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

# User Based Imports
from flask_login import current_user
from carplanner.models import User




class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    parola = PasswordField('Parola', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    numeUser = StringField('Nume', validators=[DataRequired()])
    prenumeUser = StringField('Prenume', validators=[DataRequired()])
    numeCompanie = StringField('Nume Companie')
    parola = PasswordField('Parola', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    parolaConfirm = PasswordField('Confirmare Parola', validators=[DataRequired()])
    submit = SubmitField('Inregistrare!')

    def validate_email(self, field):
        # Check if not None for that user email!
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('Your email has been registered already!')


class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    numeUser = StringField('Nume', validators=[DataRequired()])
    prenumeUser = StringField('Prenume', validators=[DataRequired()])
    numeCompanie = StringField('Nume Companie')
    picture = FileField('Incarca fotografie de profil', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Actualizeaza')

    def validate_email(self, field):
        # Check if not None for that user email!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')
