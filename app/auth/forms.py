from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp


class LoginForm(FlaskForm):
    email = StringField("Correo electrónico", validators=[DataRequired(), Email()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    recordarme = BooleanField("Recordarme")


class RegistroForm(FlaskForm):
    nombre = StringField("Nombre completo", validators=[DataRequired(), Length(max=120)])
    email = StringField("Correo electrónico", validators=[DataRequired(), Email(), Length(max=150)])
    cedula = StringField(
        "Cédula",
        validators=[DataRequired(), Regexp(r"^\d{10}$", message="La cédula debe tener 10 dígitos")],
    )
    rol = SelectField(
        "Rol",
        choices=[("deportista", "Deportista"), ("dirigente", "Dirigente Barrial")],
        validators=[DataRequired()],
    )
    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(),
            Length(min=8, message="La contraseña debe tener al menos 8 caracteres"),
        ],
    )
    confirmar_password = PasswordField(
        "Confirmar contraseña",
        validators=[DataRequired(), EqualTo("password", message="Las contraseñas no coinciden")],
    )
