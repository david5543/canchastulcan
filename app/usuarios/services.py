from app.extensions import db
from app.models.usuario import Usuario


def listar_usuarios():
    return Usuario.query.order_by(Usuario.nombre).all()


def obtener_usuario(usuario_id):
    return Usuario.query.get_or_404(usuario_id)


def actualizar_rol(usuario, nuevo_rol):
    usuario.rol = nuevo_rol
    db.session.commit()
    return usuario


def alternar_bloqueo(usuario):
    usuario.bloqueado = not usuario.bloqueado
    if not usuario.bloqueado:
        usuario.intentos_fallidos = 0
    db.session.commit()
    return usuario


def eliminar_usuario(usuario):
    db.session.delete(usuario)
    db.session.commit()
