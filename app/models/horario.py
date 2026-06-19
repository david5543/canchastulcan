from app.extensions import db


class EstadoHorarioEnum:
    LIBRE = "libre"
    OCUPADO = "ocupado"
    PENDIENTE_PAGO = "pendiente_pago"
    VALIDANDO = "validando"

    OPCIONES = [LIBRE, OCUPADO, PENDIENTE_PAGO, VALIDANDO]


class Horario(db.Model):
    __tablename__ = "horarios"

    id = db.Column(db.Integer, primary_key=True)
    cancha_id = db.Column(
        db.Integer, db.ForeignKey("canchas.id", ondelete="CASCADE"), nullable=False
    )
    hora = db.Column(db.Time, nullable=False)
    estado = db.Column(db.String(20), nullable=False, default=EstadoHorarioEnum.LIBRE)
    reserva_id = db.Column(
        db.Integer, db.ForeignKey("reservas.id", ondelete="SET NULL"), nullable=True
    )

    cancha = db.relationship("Cancha", back_populates="horarios")
    reserva = db.relationship("Reserva", back_populates="horarios")

    __table_args__ = (
        db.UniqueConstraint("cancha_id", "hora", name="uq_horario_cancha_hora"),
        db.CheckConstraint(
            "estado IN ('libre', 'ocupado', 'pendiente_pago', 'validando')",
            name="ck_horarios_estado",
        ),
        db.Index("ix_horarios_cancha_estado", "cancha_id", "estado"),
    )

    def __repr__(self):
        return f"<Horario cancha={self.cancha_id} hora={self.hora} estado={self.estado}>"
