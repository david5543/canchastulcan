from flask import current_app
from app.extensions import db
from app.models.usuario import Usuario


class CredencialesInvalidasError(Exception):
    pass


class CuentaBloqueadaError(Exception):
    pass


def registrar_usuario(nombre, email, cedula, rol, password):
    usuario = Usuario(nombre=nombre, email=email.lower().strip(), cedula=cedula, rol=rol)
    usuario.set_password(password)
    db.session.add(usuario)
    db.session.commit()
    return usuario


def email_disponible(email):
    return Usuario.query.filter_by(email=email.lower().strip()).first() is None


def cedula_disponible(cedula):
    return Usuario.query.filter_by(cedula=cedula).first() is None


def autenticar_usuario(email, password):
    usuario = Usuario.query.filter_by(email=email.lower().strip()).first()
    if usuario is None:
        raise CredencialesInvalidasError("Correo o contraseña incorrectos")

    if usuario.bloqueado:
        raise CuentaBloqueadaError("La cuenta está bloqueada por demasiados intentos fallidos")

    if not usuario.check_password(password):
        usuario.intentos_fallidos += 1
        max_intentos = current_app.config["MAX_INTENTOS_FALLIDOS"]
        if usuario.intentos_fallidos >= max_intentos:
            usuario.bloqueado = True
        db.session.commit()
        raise CredencialesInvalidasError("Correo o contraseña incorrectos")

    usuario.intentos_fallidos = 0
    db.session.commit()
    return usuario
