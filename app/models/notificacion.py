from datetime import datetime
from app.extensions import db


class Notificacion(db.Model):
    __tablename__ = "notificaciones"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(
        db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False
    )
    titulo = db.Column(db.String(150), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    leida = db.Column(db.Boolean, nullable=False, default=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    usuario = db.relationship("Usuario", back_populates="notificaciones")

    __table_args__ = (
        db.Index("ix_notificaciones_usuario_leida", "usuario_id", "leida"),
    )

    def __repr__(self):
        return f"<Notificacion {self.titulo} usuario={self.usuario_id}>"
