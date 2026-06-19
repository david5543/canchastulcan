from datetime import datetime
from app.extensions import db


class TipoOcupacionEnum:
    INSTITUCIONAL = "institucional"
    CAMPEONATO = "campeonato"
    MANTENIMIENTO = "mantenimiento"

    OPCIONES = [INSTITUCIONAL, CAMPEONATO, MANTENIMIENTO]


class OcupacionEspecial(db.Model):
    __tablename__ = "ocupaciones_especiales"

    id = db.Column(db.Integer, primary_key=True)
    cancha_id = db.Column(
        db.Integer, db.ForeignKey("canchas.id", ondelete="CASCADE"), nullable=False
    )
    fecha = db.Column(db.Date, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)
    creado_por = db.Column(
        db.Integer, db.ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True
    )
    fecha_registro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    cancha = db.relationship("Cancha", back_populates="ocupaciones")
    creador = db.relationship("Usuario", back_populates="ocupaciones_creadas")

    __table_args__ = (
        db.CheckConstraint(
            "tipo IN ('institucional', 'campeonato', 'mantenimiento')",
            name="ck_ocupaciones_tipo",
        ),
        db.CheckConstraint("hora_fin > hora_inicio", name="ck_ocupaciones_horas_validas"),
        db.Index("ix_ocupaciones_cancha_fecha", "cancha_id", "fecha"),
    )

    def __repr__(self):
        return f"<OcupacionEspecial {self.tipo} {self.fecha}>"
