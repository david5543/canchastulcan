from app.extensions import db
from app.models.orden_pago import OrdenPago, EstadoPagoEnum
from app.models.reserva import Reserva, EstadoReservaEnum
from app.utils.helpers import archivo_permitido, guardar_comprobante
from app.notifications.services import crear_notificacion


class PagoInvalidoError(Exception):
    pass


def crear_orden_pago(reserva):
    orden = OrdenPago(reserva_id=reserva.id, monto=reserva.monto, estado_pago=EstadoPagoEnum.PENDIENTE)
    db.session.add(orden)
    db.session.commit()
    return orden


def obtener_orden_por_reserva(reserva_id):
    return OrdenPago.query.filter_by(reserva_id=reserva_id).first_or_404()


def subir_comprobante(reserva, archivo):
    if reserva.estado != EstadoReservaEnum.PENDIENTE_PAGO:
        raise PagoInvalidoError("Esta reserva no admite carga de comprobante en su estado actual.")

    if archivo is None or archivo.filename == "":
        raise PagoInvalidoError("Debes seleccionar un archivo de comprobante.")

    if not archivo_permitido(archivo.filename):
        raise PagoInvalidoError("Formato de archivo no permitido (use PNG, JPG o PDF).")

    nombre_archivo = guardar_comprobante(archivo)
    reserva.comprobante = nombre_archivo
    reserva.estado = EstadoReservaEnum.VALIDANDO

    orden = reserva.orden_pago
    if orden:
        orden.estado_pago = EstadoPagoEnum.VALIDANDO

    db.session.commit()
    return reserva


def listar_pendientes():
    return (
        Reserva.query.filter_by(estado=EstadoReservaEnum.VALIDANDO)
        .order_by(Reserva.fecha_creacion.asc())
        .all()
    )


def validar_pago(reserva, aprobado):
    if reserva.estado != EstadoReservaEnum.VALIDANDO:
        raise PagoInvalidoError("Esta reserva no tiene un comprobante pendiente de validación.")

    orden = reserva.orden_pago

    if aprobado:
        reserva.estado = EstadoReservaEnum.CONFIRMADA
        if orden:
            orden.estado_pago = EstadoPagoEnum.APROBADO
        crear_notificacion(
            reserva.usuario_id,
            "Pago aprobado",
            f"Tu reserva del {reserva.fecha.strftime('%d/%m/%Y')} a las {reserva.hora.strftime('%H:%M')} fue confirmada.",
        )
    else:
        reserva.estado = EstadoReservaEnum.PENDIENTE_PAGO
        reserva.comprobante = None
        if orden:
            orden.estado_pago = EstadoPagoEnum.RECHAZADO
        crear_notificacion(
            reserva.usuario_id,
            "Comprobante rechazado",
            f"El comprobante de tu reserva del {reserva.fecha.strftime('%d/%m/%Y')} fue rechazado. Sube uno nuevo.",
        )

    db.session.commit()
    return reserva
