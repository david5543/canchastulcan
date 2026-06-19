from datetime import datetime
from flask import Blueprint, render_template, request, Response
from flask_login import login_required

from app.utils.decorators import roles_requeridos
from app.models.usuario import RolEnum
from app.models.reserva import EstadoReservaEnum
from app.reportes.services import (
    reservas_filtradas,
    generar_csv_reservas,
    generar_csv_ocupaciones,
)

reportes_bp = Blueprint("reportes", __name__, url_prefix="/reportes", template_folder="templates")


def _parsear_fecha(valor):
    return datetime.strptime(valor, "%Y-%m-%d").date() if valor else None


@reportes_bp.route("/")
@login_required
@roles_requeridos(RolEnum.ADMIN, RolEnum.DIRIGENTE)
def index():
    fecha_inicio = _parsear_fecha(request.args.get("fecha_inicio"))
    fecha_fin = _parsear_fecha(request.args.get("fecha_fin"))
    estado = request.args.get("estado") or None

    reservas = reservas_filtradas(fecha_inicio, fecha_fin, estado)
    return render_template(
        "reportes/index.html",
        reservas=reservas,
        estados=EstadoReservaEnum.OPCIONES,
        fecha_inicio=request.args.get("fecha_inicio", ""),
        fecha_fin=request.args.get("fecha_fin", ""),
        estado_seleccionado=estado,
    )


@reportes_bp.route("/reservas.csv")
@login_required
@roles_requeridos(RolEnum.ADMIN, RolEnum.DIRIGENTE)
def exportar_reservas_csv():
    fecha_inicio = _parsear_fecha(request.args.get("fecha_inicio"))
    fecha_fin = _parsear_fecha(request.args.get("fecha_fin"))
    estado = request.args.get("estado") or None

    reservas = reservas_filtradas(fecha_inicio, fecha_fin, estado)
    contenido = generar_csv_reservas(reservas)
    return Response(
        contenido,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=reservas.csv"},
    )


@reportes_bp.route("/ocupaciones.csv")
@login_required
@roles_requeridos(RolEnum.ADMIN, RolEnum.DIRIGENTE)
def exportar_ocupaciones_csv():
    contenido = generar_csv_ocupaciones()
    return Response(
        contenido,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=ocupaciones.csv"},
    )
