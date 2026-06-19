from datetime import datetime
from app.extensions import db


class EstadoReservaEnum:
    PENDIENTE_PAGO = "pendiente_pago"
    VALIDANDO = "validando"
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"

    OPCIONES = [PENDIENTE_PAGO, VALIDANDO, CONFIRMADA, CANCELADA]


class Reserva(db.Model):
    __tablename__ = "reservas"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(
        db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False
    )
    cancha_id = db.Column(
        db.Integer, db.ForeignKey("canchas.id", ondelete="CASCADE"), nullable=False
    )
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    monto = db.Column(db.Numeric(8, 2), nullable=False, default=0)
    estado = db.Column(db.String(20), nullable=False, default=EstadoReservaEnum.PENDIENTE_PAGO)
    comprobante = db.Column(db.String(255), nullable=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    usuario = db.relationship("Usuario", back_populates="reservas")
    cancha = db.relationship("Cancha", back_populates="reservas")
    horarios = db.relationship("Horario", back_populates="reserva", lazy="dynamic")
    orden_pago = db.relationship(
        "OrdenPago", back_populates="reserva", uselist=False, cascade="all, delete-orphan"
    )

    __table_args__ = (
        db.UniqueConstraint("cancha_id", "fecha", "hora", name="uq_reserva_cancha_fecha_hora"),
        db.CheckConstraint(
            "estado IN ('pendiente_pago', 'validando', 'confirmada', 'cancelada')",
            name="ck_reservas_estado",
        ),
        db.CheckConstraint("monto >= 0", name="ck_reservas_monto_positivo"),
        db.Index("ix_reservas_usuario_estado", "usuario_id", "estado"),
        db.Index("ix_reservas_cancha_fecha", "cancha_id", "fecha"),
    )

    def __repr__(self):
        return f"<Reserva {self.id} {self.fecha} {self.hora} {self.estado}>"
