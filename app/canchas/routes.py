from decimal import Decimal, InvalidOperation
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required

from app.utils.decorators import roles_requeridos
from app.models.usuario import RolEnum
from app.models.cancha import EstadoCanchaEnum
from app.canchas.services import (
    listar_canchas,
    obtener_cancha,
    crear_cancha,
    actualizar_cancha,
    eliminar_cancha,
)

canchas_bp = Blueprint("canchas", __name__, url_prefix="/canchas", template_folder="templates")


def _leer_datos_formulario():
    try:
        precio = Decimal(request.form.get("precio", "0"))
    except InvalidOperation:
        precio = Decimal("0")
    return {
        "nombre": request.form.get("nombre", "").strip(),
        "tipo": request.form.get("tipo", "").strip(),
        "zona": request.form.get("zona", "").strip(),
        "acceso": request.form.get("acceso", "").strip(),
        "precio": precio,
        "especialidad": request.form.get("especialidad", "").strip(),
        "estado": request.form.get("estado", EstadoCanchaEnum.DISPONIBLE),
    }


@canchas_bp.route("/")
@login_required
def listar():
    canchas = listar_canchas()
    return render_template("canchas/listar.html", canchas=canchas)


@canchas_bp.route("/nueva", methods=["GET", "POST"])
@login_required
@roles_requeridos(RolEnum.ADMIN, RolEnum.DIRIGENTE)
def nueva():
    if request.method == "POST":
        datos = _leer_datos_formulario()
        if not datos["nombre"] or not datos["tipo"] or not datos["zona"]:
            flash("Nombre, tipo y zona son obligatorios.", "danger")
        else:
            crear_cancha(datos)
            flash("Cancha creada correctamente.", "success")
            return redirect(url_for("canchas.listar"))
    return render_template("canchas/formulario.html", cancha=None, estados=EstadoCanchaEnum.OPCIONES)


@canchas_bp.route("/<int:cancha_id>/editar", methods=["GET", "POST"])
@login_required
@roles_requeridos(RolEnum.ADMIN, RolEnum.DIRIGENTE)
def editar(cancha_id):
    cancha = obtener_cancha(cancha_id)
    if request.method == "POST":
        datos = _leer_datos_formulario()
        if not datos["nombre"] or not datos["tipo"] or not datos["zona"]:
            flash("Nombre, tipo y zona son obligatorios.", "danger")
        else:
            actualizar_cancha(cancha, datos)
            flash("Cancha actualizada correctamente.", "success")
            return redirect(url_for("canchas.listar"))
    return render_template("canchas/formulario.html", cancha=cancha, estados=EstadoCanchaEnum.OPCIONES)


@canchas_bp.route("/<int:cancha_id>/eliminar", methods=["POST"])
@login_required
@roles_requeridos(RolEnum.ADMIN)
def eliminar(cancha_id):
    cancha = obtener_cancha(cancha_id)
    eliminar_cancha(cancha)
    flash("Cancha eliminada correctamente.", "success")
    return redirect(url_for("canchas.listar"))
