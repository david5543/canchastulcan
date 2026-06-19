from datetime import datetime, date
from app.extensions import db
from app.models.cancha import Cancha
from app.models.horario import Horario, EstadoHorarioEnum
from app.models.reserva import Reserva, EstadoReservaEnum
from app.models.ocupacion import OcupacionEspecial
from app.models.usuario import RolEnum
from app.utils.helpers import dias_semana

COLOR_OCUPACION = {
    "institucional": "primary",
    "campeonato": "purple",
    "mantenimiento": "secondary",
}

COLOR_HORARIO = {
    EstadoHorarioEnum.LIBRE: "success",
    EstadoHorarioEnum.OCUPADO: "danger",
    EstadoHorarioEnum.PENDIENTE_PAGO: "warning",
    EstadoHorarioEnum.VALIDANDO: "orange",
}


class ReservaInvalidaError(Exception):
    pass


def _ocupacion_en_horario(cancha_id, fecha, hora):
    return (
        OcupacionEspecial.query.filter(
            OcupacionEspecial.cancha_id == cancha_id,
            OcupacionEspecial.fecha == fecha,
            OcupacionEspecial.hora_inicio <= hora,
            OcupacionEspecial.hora_fin > hora,
        ).first()
    )


def construir_calendario_semanal(cancha_id, fecha_referencia=None):
    cancha = Cancha.query.get_or_404(cancha_id)
    semana = dias_semana(fecha_referencia)
    horarios_base = cancha.horarios.order_by(Horario.hora).all()

    calendario = []
    for dia in semana:
        celdas = []
        for horario in horarios_base:
            ocupacion = _ocupacion_en_horario(cancha_id, dia, horario.hora)
            reserva_del_dia = Reserva.query.filter_by(
                cancha_id=cancha_id, fecha=dia, hora=horario.hora
            ).filter(Reserva.estado != EstadoReservaEnum.CANCELADA).first()

            if ocupacion:
                estado = ocupacion.tipo
                color = COLOR_OCUPACION[ocupacion.tipo]
                reserva_id = None
                reservable = False
            elif reserva_del_dia:
                estado = reserva_del_dia.estado
                color = COLOR_HORARIO.get(
                    EstadoHorarioEnum.OCUPADO
                    if estado == EstadoReservaEnum.CONFIRMADA
                    else (
                        EstadoHorarioEnum.PENDIENTE_PAGO
                        if estado == EstadoReservaEnum.PENDIENTE_PAGO
                        else EstadoHorarioEnum.VALIDANDO
                    )
                )
                reserva_id = reserva_del_dia.id
                reservable = False
            else:
                estado = EstadoHorarioEnum.LIBRE
                color = COLOR_HORARIO[EstadoHorarioEnum.LIBRE]
                reserva_id = None
                reservable = dia >= date.today()

            celdas.append(
                {
                    "hora": horario.hora,
                    "estado": estado,
                    "color": color,
                    "reserva_id": reserva_id,
                    "reservable": reservable,
                }
            )
        calendario.append({"fecha": dia, "celdas": celdas})

    return cancha, calendario


def crear_reserva(usuario, cancha_id, fecha, hora):
    cancha = Cancha.query.get_or_404(cancha_id)

    if fecha < date.today():
        raise ReservaInvalidaError("No se puede reservar una fecha pasada.")

    if _ocupacion_en_horario(cancha_id, fecha, hora):
        raise ReservaInvalidaError("Ese horario está bloqueado por una ocupación especial.")

    existente = Reserva.query.filter_by(cancha_id=cancha_id, fecha=fecha, hora=hora).filter(
        Reserva.estado != EstadoReservaEnum.CANCELADA
    ).first()
    if existente:
        raise ReservaInvalidaError("Ese horario ya está reservado.")

    reserva = Reserva(
        usuario_id=usuario.id,
        cancha_id=cancha_id,
        fecha=fecha,
        hora=hora,
        monto=cancha.precio,
        estado=EstadoReservaEnum.PENDIENTE_PAGO,
    )
    db.session.add(reserva)
    db.session.commit()

    from app.pagos.services import crear_orden_pago

    crear_orden_pago(reserva)
    return reserva


def cancelar_reserva(reserva, usuario):
    if usuario.rol == RolEnum.DEPORTISTA and reserva.usuario_id != usuario.id:
        raise ReservaInvalidaError("No puedes cancelar una reserva que no es tuya.")

    if reserva.estado == EstadoReservaEnum.CANCELADA:
        raise ReservaInvalidaError("La reserva ya está cancelada.")

    reserva.estado = EstadoReservaEnum.CANCELADA
    db.session.commit()
    return reserva


def obtener_reserva(reserva_id):
    return Reserva.query.get_or_404(reserva_id)


def historial_reservas(usuario):
    consulta = Reserva.query.order_by(Reserva.fecha_creacion.desc())
    if usuario.rol == RolEnum.DEPORTISTA:
        consulta = consulta.filter_by(usuario_id=usuario.id)
    return consulta.all()
