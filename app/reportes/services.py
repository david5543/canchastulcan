import csv
import io
from datetime import datetime
from app.models.reserva import Reserva
from app.models.ocupacion import OcupacionEspecial


def _aplicar_filtros_fecha(consulta, columna_fecha, fecha_inicio, fecha_fin):
    if fecha_inicio:
        consulta = consulta.filter(columna_fecha >= fecha_inicio)
    if fecha_fin:
        consulta = consulta.filter(columna_fecha <= fecha_fin)
    return consulta


def reservas_filtradas(fecha_inicio=None, fecha_fin=None, estado=None):
    consulta = Reserva.query
    consulta = _aplicar_filtros_fecha(consulta, Reserva.fecha, fecha_inicio, fecha_fin)
    if estado:
        consulta = consulta.filter(Reserva.estado == estado)
    return consulta.order_by(Reserva.fecha.desc()).all()


def generar_csv_reservas(reservas):
    buffer = io.StringIO()
    escritor = csv.writer(buffer)
    escritor.writerow(
        ["ID", "Usuario", "Cancha", "Fecha", "Hora", "Monto", "Estado", "Fecha de creación"]
    )
    for reserva in reservas:
        escritor.writerow(
            [
                reserva.id,
                reserva.usuario.nombre,
                reserva.cancha.nombre,
                reserva.fecha.strftime("%Y-%m-%d"),
                reserva.hora.strftime("%H:%M"),
                f"{reserva.monto:.2f}",
                reserva.estado,
                reserva.fecha_creacion.strftime("%Y-%m-%d %H:%M"),
            ]
        )
    buffer.seek(0)
    return buffer.getvalue()


def generar_csv_ocupaciones():
    ocupaciones = OcupacionEspecial.query.order_by(OcupacionEspecial.fecha.desc()).all()
    buffer = io.StringIO()
    escritor = csv.writer(buffer)
    escritor.writerow(["ID", "Cancha", "Fecha", "Hora inicio", "Hora fin", "Tipo", "Descripción"])
    for ocupacion in ocupaciones:
        escritor.writerow(
            [
                ocupacion.id,
                ocupacion.cancha.nombre,
                ocupacion.fecha.strftime("%Y-%m-%d"),
                ocupacion.hora_inicio.strftime("%H:%M"),
                ocupacion.hora_fin.strftime("%H:%M"),
                ocupacion.tipo,
                ocupacion.descripcion or "",
            ]
        )
    buffer.seek(0)
    return buffer.getvalue()
