from datetime import date
from flask import Blueprint, render_template
from flask_login import login_required, current_user

from app.models.cancha import Cancha
from app.models.reserva import Reserva, EstadoReservaEnum
from app.models.usuario import Usuario, RolEnum

dashboard_bp = Blueprint("dashboard", __name__, template_folder="templates")


@dashboard_bp.route("/")
@login_required
def index():
    contexto = {}

    if current_user.rol == RolEnum.ADMIN:
        contexto["total_canchas"] = Cancha.query.count()
        contexto["total_usuarios"] = Usuario.query.count()
        contexto["reservas_pendientes_pago"] = Reserva.query.filter_by(
            estado=EstadoReservaEnum.PENDIENTE_PAGO
        ).count()
        contexto["reservas_validando"] = Reserva.query.filter_by(
            estado=EstadoReservaEnum.VALIDANDO
        ).count()
        contexto["reservas_confirmadas_hoy"] = Reserva.query.filter_by(
            estado=EstadoReservaEnum.CONFIRMADA, fecha=date.today()
        ).count()
    elif current_user.rol == RolEnum.DIRIGENTE:
        contexto["total_canchas"] = Cancha.query.count()
        contexto["reservas_confirmadas_hoy"] = Reserva.query.filter_by(
            estado=EstadoReservaEnum.CONFIRMADA, fecha=date.today()
        ).count()
    else:
        contexto["mis_reservas_activas"] = Reserva.query.filter(
            Reserva.usuario_id == current_user.id,
            Reserva.estado.in_(
                [EstadoReservaEnum.PENDIENTE_PAGO, EstadoReservaEnum.VALIDANDO, EstadoReservaEnum.CONFIRMADA]
            ),
        ).count()

    return render_template("dashboard/index.html", **contexto)
