from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app.utils.decorators import roles_requeridos
from app.models.usuario import RolEnum
from app.reservas.services import obtener_reserva
from app.pagos.services import (
    obtener_orden_por_reserva,
    subir_comprobante,
    listar_pendientes as servicio_listar_pendientes,
    validar_pago,
    PagoInvalidoError,
)

pagos_bp = Blueprint("pagos", __name__, url_prefix="/pagos", template_folder="templates")


@pagos_bp.route("/orden/<int:reserva_id>", methods=["GET", "POST"])
@login_required
def orden(reserva_id):
    reserva = obtener_reserva(reserva_id)

    if current_user.rol == RolEnum.DEPORTISTA and reserva.usuario_id != current_user.id:
        flash("No puedes acceder a la orden de pago de otro usuario.", "danger")
        return redirect(url_for("reservas.historial"))

    orden_pago = obtener_orden_por_reserva(reserva_id)

    if request.method == "POST":
        archivo = request.files.get("comprobante")
        try:
            subir_comprobante(reserva, archivo)
            flash("Comprobante enviado. Será validado por un administrador.", "success")
            return redirect(url_for("reservas.historial"))
        except PagoInvalidoError as error:
            flash(str(error), "danger")

    return render_template("pagos/orden.html", reserva=reserva, orden=orden_pago)


@pagos_bp.route("/pendientes")
@login_required
@roles_requeridos(RolEnum.ADMIN)
def listar_pendientes():
    reservas = servicio_listar_pendientes()
    return render_template("pagos/pendientes.html", reservas=reservas)


@pagos_bp.route("/<int:reserva_id>/validar", methods=["POST"])
@login_required
@roles_requeridos(RolEnum.ADMIN)
def validar(reserva_id):
    reserva = obtener_reserva(reserva_id)
    aprobado = request.form.get("decision") == "aprobar"
    try:
        validar_pago(reserva, aprobado)
        flash("Pago validado correctamente.", "success")
    except PagoInvalidoError as error:
        flash(str(error), "danger")
    return redirect(url_for("pagos.listar_pendientes"))
