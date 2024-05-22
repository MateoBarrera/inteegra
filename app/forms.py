"""INTEGRA 2023 Platform Server Forms File

This file is part of the INTEGRA 2023 platform flask server.
It integrates the data model for the User's session information required for the server built-in login.

@Author: Mateo Barrera

@Date: 12-07-2022
"""
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, BooleanField, EmailField
from wtforms.validators import DataRequired, EqualTo, InputRequired, Length, Optional, Email


class LoginForm(FlaskForm):
    username = EmailField('Correo electrónico', validators=[InputRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField("Recuérdame", validators=[Optional()])
    submit = SubmitField('Iniciar sesión')


class SignupForm(FlaskForm):
    first_name = StringField('Nombre', validators=[InputRequired()])
    last_name = StringField('Apellido', validators=[InputRequired()])
    username = StringField('Correo electrónico', validators=[
        InputRequired(), Email()])
    password = PasswordField('Contraseña', validators=[
        InputRequired(), Length(min=4, max=25)])
    password_confirm = PasswordField(
        'Confirmar Contraseña',
        validators=[InputRequired(), EqualTo('password', message='Las contraseñas no coinciden'),
                    Length(min=4, max=25)])
    terms = BooleanField(
        "Autorizo política de tratamiento de datos personales *", validators=[DataRequired()])
    submit = SubmitField('Registrarse')


class RecoveryForm(FlaskForm):
    email = EmailField('Correo registrado', validators=[InputRequired(
        "Ingrese su dirección de correo"), Email()])
    submit = SubmitField('Enviar')
