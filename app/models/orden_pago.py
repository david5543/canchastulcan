import uuid
from datetime import datetime
from app.extensions import db


class EstadoPagoEnum:
    PENDIENTE = "pendiente"
    VALIDANDO = "validando"
    APROBADO = "aprobado"
    RECHAZADO = "rechazado"

    OPCIONES = [PENDIENTE, VALIDANDO, APROBADO, RECHAZADO]


def generar_codigo_orden():
    return f"OP-{uuid.uuid4().hex[:10].upper()}"


class OrdenPago(db.Model):
    __tablename__ = "ordenes_pago"

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(30), nullable=False, unique=True, default=generar_codigo_orden)
    reserva_id = db.Column(
        db.Integer, db.ForeignKey("reservas.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    monto = db.Column(db.Numeric(8, 2), nullable=False, default=0)
    estado_pago = db.Column(db.String(20), nullable=False, default=EstadoPagoEnum.PENDIENTE)
    fecha_generacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    reserva = db.relationship("Reserva", back_populates="orden_pago")

    __table_args__ = (
        db.CheckConstraint(
            "estado_pago IN ('pendiente', 'validando', 'aprobado', 'rechazado')",
            name="ck_ordenes_pago_estado",
        ),
        db.CheckConstraint("monto >= 0", name="ck_ordenes_pago_monto_positivo"),
    )

    def __repr__(self):
        return f"<OrdenPago {self.codigo} {self.estado_pago}>"
