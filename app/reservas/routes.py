from datetime import datetime, timedelta, date
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app.canchas.services import listar_canchas
from app.reservas.services import (
    construir_calendario_semanal,
    crear_reserva,
    cancelar_reserva,
    obtener_reserva,
    historial_reservas,
    ReservaInvalidaError,
)

reservas_bp = Blueprint("reservas", __name__, url_prefix="/reservas", template_folder="templates")


@reservas_bp.route("/calendario")
@login_required
def calendario():
    canchas = listar_canchas()
    if not canchas:
        flash("No hay canchas registradas todavía.", "info")
        return render_template("reservas/calendario.html", canchas=[], cancha=None, calendario=[])

    cancha_id = request.args.get("cancha_id", type=int) or canchas[0].id

    semana_offset = request.args.get("semana", default=0, type=int)
    fecha_referencia = date.today() + timedelta(weeks=semana_offset)

    cancha, semana = construir_calendario_semanal(cancha_id, fecha_referencia)

    return render_template(
        "reservas/calendario.html",
        canchas=canchas,
        cancha=cancha,
        calendario=semana,
        semana_offset=semana_offset,
    )


@reservas_bp.route("/reservar", methods=["POST"])
@login_required
def reservar():
    cancha_id = request.form.get("cancha_id", type=int)
    fecha_str = request.form.get("fecha")
    hora_str = request.form.get("hora")
    semana_offset = request.form.get("semana_offset", default=0, type=int)

    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        hora = datetime.strptime(hora_str, "%H:%M").time()
        crear_reserva(current_user, cancha_id, fecha, hora)
        flash("Reserva creada. Genera y paga tu orden de pago para confirmarla.", "success")
    except ReservaInvalidaError as error:
        flash(str(error), "danger")
    except (ValueError, TypeError):
        flash("Datos de reserva inválidos.", "danger")

    return redirect(url_for("reservas.calendario", cancha_id=cancha_id, semana=semana_offset))


@reservas_bp.route("/<int:reserva_id>/cancelar", methods=["POST"])
@login_required
def cancelar(reserva_id):
    reserva = obtener_reserva(reserva_id)
    try:
        cancelar_reserva(reserva, current_user)
        flash("Reserva cancelada correctamente.", "success")
    except ReservaInvalidaError as error:
        flash(str(error), "danger")
    return redirect(url_for("reservas.historial"))


@reservas_bp.route("/historial")
@login_required
def historial():
    reservas = historial_reservas(current_user)
    return render_template("reservas/historial.html", reservas=reservas)
