from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.notifications.services import (
    listar_notificaciones,
    marcar_como_leida,
    marcar_todas_leidas,
)

notifications_bp = Blueprint(
    "notifications", __name__, url_prefix="/notificaciones", template_folder="templates"
)


@notifications_bp.route("/")
@login_required
def listar():
    notificaciones = listar_notificaciones(current_user)
    return render_template("notifications/listar.html", notificaciones=notificaciones)


@notifications_bp.route("/<int:notificacion_id>/leer", methods=["POST"])
@login_required
def leer(notificacion_id):
    marcar_como_leida(notificacion_id, current_user)
    return redirect(url_for("notifications.listar"))


@notifications_bp.route("/leer-todas", methods=["POST"])
@login_required
def leer_todas():
    marcar_todas_leidas(current_user)
    flash("Todas las notificaciones fueron marcadas como leídas.", "success")
    return redirect(url_for("notifications.listar"))
