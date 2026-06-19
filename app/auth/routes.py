from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from app.auth.forms import LoginForm, RegistroForm
from app.auth.services import (
    registrar_usuario,
    autenticar_usuario,
    email_disponible,
    cedula_disponible,
    CredencialesInvalidasError,
    CuentaBloqueadaError,
)

auth_bp = Blueprint("auth", __name__, url_prefix="/auth", template_folder="templates")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = LoginForm()
    if form.validate_on_submit():
        try:
            usuario = autenticar_usuario(form.email.data, form.password.data)
            login_user(usuario, remember=form.recordarme.data)
            siguiente = request.args.get("next")
            return redirect(siguiente or url_for("dashboard.index"))
        except (CredencialesInvalidasError, CuentaBloqueadaError) as error:
            flash(str(error), "danger")

    return render_template("auth/login.html", form=form)


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = RegistroForm()
    if form.validate_on_submit():
        if not email_disponible(form.email.data):
            flash("Ese correo electrónico ya está registrado.", "danger")
        elif not cedula_disponible(form.cedula.data):
            flash("Esa cédula ya está registrada.", "danger")
        else:
            registrar_usuario(
                nombre=form.nombre.data,
                email=form.email.data,
                cedula=form.cedula.data,
                rol=form.rol.data,
                password=form.password.data,
            )
            flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
            return redirect(url_for("auth.login"))

    return render_template("auth/registro.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("auth.login"))
