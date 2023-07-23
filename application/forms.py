from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from application.models import Editors

class LoginForm(FlaskForm):
    editor   = StringField("DNI del editor", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8,max=16)])
    remember_me = BooleanField("Recordarme")
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    editor   = StringField("DNI del editor", validators=[DataRequired(), Length(min=8,max=9)])
    password = PasswordField("Password", validators=[DataRequired(),Length(min=8,max=16)])
    password_confirm = PasswordField("Confirme Password", validators=[DataRequired(),Length(min=8,max=16), EqualTo('password')])
    first_name = StringField("Primer nombre", validators=[DataRequired(),Length(min=2,max=40)])
    pat_name = StringField("Primer apellido", validators=[DataRequired(),Length(min=2,max=50)])
    mat_name = StringField("Segundo apellido", validators=[DataRequired(),Length(min=2,max=50)])
    submit = SubmitField("Registrese ahora")

    def validate_editor(self, editor):
        user = Editors.query.filter_by(edt_usr_id=editor.data).first()
        if user:
            raise ValidationError("Usuario ya está en uso. Elija otro.")