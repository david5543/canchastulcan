from app.extensions import db
from app.models.ocupacion import OcupacionEspecial


class OcupacionInvalidaError(Exception):
    pass


def listar_ocupaciones():
    return OcupacionEspecial.query.order_by(OcupacionEspecial.fecha.desc()).all()


def obtener_ocupacion(ocupacion_id):
    return OcupacionEspecial.query.get_or_404(ocupacion_id)


def crear_ocupacion(datos, creado_por):
    if datos["hora_fin"] <= datos["hora_inicio"]:
        raise OcupacionInvalidaError("La hora de fin debe ser posterior a la hora de inicio.")

    ocupacion = OcupacionEspecial(
        cancha_id=datos["cancha_id"],
        fecha=datos["fecha"],
        hora_inicio=datos["hora_inicio"],
        hora_fin=datos["hora_fin"],
        tipo=datos["tipo"],
        descripcion=datos.get("descripcion"),
        creado_por=creado_por,
    )
    db.session.add(ocupacion)
    db.session.commit()
    return ocupacion


def eliminar_ocupacion(ocupacion):
    db.session.delete(ocupacion)
    db.session.commit()
