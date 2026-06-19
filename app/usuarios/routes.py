from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app.utils.decorators import roles_requeridos
from app.models.usuario import RolEnum
from app.usuarios.services import (
    listar_usuarios,
    obtener_usuario,
    actualizar_rol,
    alternar_bloqueo,
    eliminar_usuario,
)

usuarios_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios", template_folder="templates")


@usuarios_bp.route("/")
@login_required
@roles_requeridos(RolEnum.ADMIN)
def listar():
    usuarios = listar_usuarios()
    return render_template("usuarios/listar.html", usuarios=usuarios, roles=RolEnum.OPCIONES)


@usuarios_bp.route("/<int:usuario_id>/rol", methods=["POST"])
@login_required
@roles_requeridos(RolEnum.ADMIN)
def cambiar_rol(usuario_id):
    usuario = obtener_usuario(usuario_id)
    nuevo_rol = request.form.get("rol")
    if nuevo_rol in RolEnum.OPCIONES:
        actualizar_rol(usuario, nuevo_rol)
        flash(f"Rol de {usuario.nombre} actualizado a {nuevo_rol}.", "success")
    else:
        flash("Rol inválido.", "danger")
    return redirect(url_for("usuarios.listar"))


@usuarios_bp.route("/<int:usuario_id>/bloqueo", methods=["POST"])
@login_required
@roles_requeridos(RolEnum.ADMIN)
def bloqueo(usuario_id):
    usuario = obtener_usuario(usuario_id)
    if usuario.id == current_user.id:
        flash("No puedes bloquear tu propia cuenta.", "danger")
    else:
        alternar_bloqueo(usuario)
        flash("Estado de bloqueo actualizado.", "success")
    return redirect(url_for("usuarios.listar"))


@usuarios_bp.route("/<int:usuario_id>/eliminar", methods=["POST"])
@login_required
@roles_requeridos(RolEnum.ADMIN)
def eliminar(usuario_id):
    usuario = obtener_usuario(usuario_id)
    if usuario.id == current_user.id:
        flash("No puedes eliminar tu propia cuenta.", "danger")
    else:
        eliminar_usuario(usuario)
        flash("Usuario eliminado correctamente.", "success")
    return redirect(url_for("usuarios.listar"))
