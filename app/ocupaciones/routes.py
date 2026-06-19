from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app.utils.decorators import roles_requeridos
from app.models.usuario import RolEnum
from app.models.ocupacion import TipoOcupacionEnum
from app.canchas.services import listar_canchas
from app.ocupaciones.services import (
    listar_ocupaciones,
    obtener_ocupacion,
    crear_ocupacion,
    eliminar_ocupacion,
    OcupacionInvalidaError,
)

ocupaciones_bp = Blueprint(
    "ocupaciones", __name__, url_prefix="/ocupaciones", template_folder="templates"
)


@ocupaciones_bp.route("/")
@login_required
@roles_requeridos(RolEnum.ADMIN, RolEnum.DIRIGENTE)
def listar():
    ocupaciones = listar_ocupaciones()
    return render_template("ocupaciones/listar.html", ocupaciones=ocupaciones)


@ocupaciones_bp.route("/nueva", methods=["GET", "POST"])
@login_required
@roles_requeridos(RolEnum.ADMIN, RolEnum.DIRIGENTE)
def nueva():
    canchas = listar_canchas()

    if request.method == "POST":
        try:
            datos = {
                "cancha_id": int(request.form.get("cancha_id")),
                "fecha": datetime.strptime(request.form.get("fecha"), "%Y-%m-%d").date(),
                "hora_inicio": datetime.strptime(request.form.get("hora_inicio"), "%H:%M").time(),
                "hora_fin": datetime.strptime(request.form.get("hora_fin"), "%H:%M").time(),
                "tipo": request.form.get("tipo"),
                "descripcion": request.form.get("descripcion", "").strip(),
            }
            crear_ocupacion(datos, current_user.id)
            flash("Ocupación especial registrada correctamente.", "success")
            return redirect(url_for("ocupaciones.listar"))
        except (ValueError, TypeError):
            flash("Datos inválidos en el formulario.", "danger")
        except OcupacionInvalidaError as error:
            flash(str(error), "danger")

    return render_template(
        "ocupaciones/formulario.html", canchas=canchas, tipos=TipoOcupacionEnum.OPCIONES
    )


@ocupaciones_bp.route("/<int:ocupacion_id>/eliminar", methods=["POST"])
@login_required
@roles_requeridos(RolEnum.ADMIN, RolEnum.DIRIGENTE)
def eliminar(ocupacion_id):
    ocupacion = obtener_ocupacion(ocupacion_id)
    eliminar_ocupacion(ocupacion)
    flash("Ocupación especial eliminada.", "success")
    return redirect(url_for("ocupaciones.listar"))
