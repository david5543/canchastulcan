from datetime import time
from app.extensions import db
from app.models.cancha import Cancha, EstadoCanchaEnum
from app.models.horario import Horario, EstadoHorarioEnum

HORA_INICIO_JORNADA = 8
HORA_FIN_JORNADA = 20


def listar_canchas():
    return Cancha.query.order_by(Cancha.nombre).all()


def obtener_cancha(cancha_id):
    return Cancha.query.get_or_404(cancha_id)


def crear_cancha(datos):
    cancha = Cancha(
        nombre=datos["nombre"],
        tipo=datos["tipo"],
        zona=datos["zona"],
        acceso=datos.get("acceso"),
        precio=datos["precio"],
        especialidad=datos.get("especialidad"),
        estado=datos.get("estado", EstadoCanchaEnum.DISPONIBLE),
    )
    db.session.add(cancha)
    db.session.commit()
    generar_horarios_base(cancha)
    return cancha


def actualizar_cancha(cancha, datos):
    cancha.nombre = datos["nombre"]
    cancha.tipo = datos["tipo"]
    cancha.zona = datos["zona"]
    cancha.acceso = datos.get("acceso")
    cancha.precio = datos["precio"]
    cancha.especialidad = datos.get("especialidad")
    cancha.estado = datos.get("estado", cancha.estado)
    db.session.commit()
    return cancha


def eliminar_cancha(cancha):
    db.session.delete(cancha)
    db.session.commit()


def generar_horarios_base(cancha):
    for hora in range(HORA_INICIO_JORNADA, HORA_FIN_JORNADA):
        horario = Horario(cancha_id=cancha.id, hora=time(hour=hora), estado=EstadoHorarioEnum.LIBRE)
        db.session.add(horario)
    db.session.commit()
