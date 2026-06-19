from app.extensions import db
from app.models.notificacion import Notificacion


def crear_notificacion(usuario_id, titulo, mensaje):
    notificacion = Notificacion(usuario_id=usuario_id, titulo=titulo, mensaje=mensaje)
    db.session.add(notificacion)
    db.session.commit()
    return notificacion


def listar_notificaciones(usuario):
    return (
        Notificacion.query.filter_by(usuario_id=usuario.id)
        .order_by(Notificacion.fecha_creacion.desc())
        .all()
    )


def contar_no_leidas(usuario):
    return Notificacion.query.filter_by(usuario_id=usuario.id, leida=False).count()


def marcar_como_leida(notificacion_id, usuario):
    notificacion = Notificacion.query.filter_by(id=notificacion_id, usuario_id=usuario.id).first()
    if notificacion:
        notificacion.leida = True
        db.session.commit()
    return notificacion


def marcar_todas_leidas(usuario):
    Notificacion.query.filter_by(usuario_id=usuario.id, leida=False).update({"leida": True})
    db.session.commit()
