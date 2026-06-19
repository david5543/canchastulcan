from datetime import datetime
from flask_login import UserMixin
from app.extensions import db, bcrypt


class RolEnum:
    DEPORTISTA = "deportista"
    DIRIGENTE = "dirigente"
    ADMIN = "admin"

    OPCIONES = [DEPORTISTA, DIRIGENTE, ADMIN]


class Usuario(db.Model, UserMixin):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default=RolEnum.DEPORTISTA)
    cedula = db.Column(db.String(10), nullable=False, unique=True)
    intentos_fallidos = db.Column(db.Integer, nullable=False, default=0)
    bloqueado = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    reservas = db.relationship("Reserva", back_populates="usuario", lazy="dynamic")
    notificaciones = db.relationship(
        "Notificacion", back_populates="usuario", lazy="dynamic",
        cascade="all, delete-orphan",
    )
    ocupaciones_creadas = db.relationship(
        "OcupacionEspecial", back_populates="creador", lazy="dynamic"
    )

    __table_args__ = (
        db.CheckConstraint(
            "rol IN ('deportista', 'dirigente', 'admin')", name="ck_usuarios_rol"
        ),
    )

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @property
    def es_admin(self):
        return self.rol == RolEnum.ADMIN

    @property
    def es_dirigente(self):
        return self.rol == RolEnum.DIRIGENTE

    @property
    def es_deportista(self):
        return self.rol == RolEnum.DEPORTISTA

    def __repr__(self):
        return f"<Usuario {self.email} ({self.rol})>"
