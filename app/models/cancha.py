from app.extensions import db


class EstadoCanchaEnum:
    DISPONIBLE = "disponible"
    MANTENIMIENTO = "mantenimiento"
    INACTIVA = "inactiva"

    OPCIONES = [DISPONIBLE, MANTENIMIENTO, INACTIVA]


class Cancha(db.Model):
    __tablename__ = "canchas"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    zona = db.Column(db.String(100), nullable=False)
    acceso = db.Column(db.String(100), nullable=True)
    precio = db.Column(db.Numeric(8, 2), nullable=False, default=0)
    especialidad = db.Column(db.String(100), nullable=True)
    estado = db.Column(db.String(20), nullable=False, default=EstadoCanchaEnum.DISPONIBLE)

    horarios = db.relationship(
        "Horario", back_populates="cancha", lazy="dynamic", cascade="all, delete-orphan"
    )
    reservas = db.relationship("Reserva", back_populates="cancha", lazy="dynamic")
    ocupaciones = db.relationship(
        "OcupacionEspecial", back_populates="cancha", lazy="dynamic",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        db.CheckConstraint("precio >= 0", name="ck_canchas_precio_positivo"),
        db.CheckConstraint(
            "estado IN ('disponible', 'mantenimiento', 'inactiva')",
            name="ck_canchas_estado",
        ),
    )

    def __repr__(self):
        return f"<Cancha {self.nombre}>"
