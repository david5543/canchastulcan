from datetime import date, timedelta, time
from decimal import Decimal

from app.extensions import db
from app.models.usuario import Usuario, RolEnum
from app.models.cancha import Cancha, EstadoCanchaEnum
from app.models.horario import Horario, EstadoHorarioEnum
from app.models.reserva import Reserva, EstadoReservaEnum
from app.models.orden_pago import OrdenPago, EstadoPagoEnum

USUARIOS_DEMO = [
    {
        "nombre": "Administrador GAD",
        "email": "admin@canchatulcan.com",
        "cedula": "0401234567",
        "rol": RolEnum.ADMIN,
    },
    {
        "nombre": "Dirigente Barrial",
        "email": "dirigente@canchatulcan.com",
        "cedula": "0407654321",
        "rol": RolEnum.DIRIGENTE,
    },
    {
        "nombre": "Deportista Demo",
        "email": "deportista@canchatulcan.com",
        "cedula": "0409876543",
        "rol": RolEnum.DEPORTISTA,
    },
]

CONTRASENA_DEMO = "Admin123*"

CANCHAS_DEMO = [
    {"nombre": "Cancha El Cóndor", "tipo": "Fútbol", "zona": "Norte", "precio": Decimal("15.00")},
    {"nombre": "Cancha La Esperanza", "tipo": "Fútbol", "zona": "Sur", "precio": Decimal("12.00")},
    {"nombre": "Cancha Central", "tipo": "Vóley", "zona": "Centro", "precio": Decimal("8.00")},
    {"nombre": "Cancha San Francisco", "tipo": "Básquet", "zona": "Norte", "precio": Decimal("10.00")},
    {"nombre": "Cancha La Delicia", "tipo": "Fútbol", "zona": "Sur", "precio": Decimal("14.00")},
    {"nombre": "Cancha González Suárez", "tipo": "Fútbol", "zona": "Centro", "precio": Decimal("13.00")},
    {"nombre": "Cancha Tulcán Norte", "tipo": "Vóley", "zona": "Norte", "precio": Decimal("7.00")},
    {"nombre": "Cancha 27 de Septiembre", "tipo": "Básquet", "zona": "Centro", "precio": Decimal("9.00")},
    {"nombre": "Cancha Las Cuadras", "tipo": "Fútbol", "zona": "Sur", "precio": Decimal("16.00")},
    {"nombre": "Cancha La Florida", "tipo": "Fútbol", "zona": "Norte", "precio": Decimal("11.00")},
]

HORA_INICIO_JORNADA = 8
HORA_FIN_JORNADA = 20


def _crear_usuarios():
    usuarios = {}
    for datos in USUARIOS_DEMO:
        usuario = Usuario(
            nombre=datos["nombre"], email=datos["email"], cedula=datos["cedula"], rol=datos["rol"]
        )
        usuario.set_password(CONTRASENA_DEMO)
        db.session.add(usuario)
        usuarios[datos["rol"]] = usuario
    db.session.commit()
    return usuarios


def _crear_canchas():
    canchas = []
    for datos in CANCHAS_DEMO:
        cancha = Cancha(
            nombre=datos["nombre"],
            tipo=datos["tipo"],
            zona=datos["zona"],
            precio=datos["precio"],
            estado=EstadoCanchaEnum.DISPONIBLE,
        )
        db.session.add(cancha)
        canchas.append(cancha)
    db.session.commit()

    for cancha in canchas:
        for hora in range(HORA_INICIO_JORNADA, HORA_FIN_JORNADA):
            db.session.add(
                Horario(cancha_id=cancha.id, hora=time(hour=hora), estado=EstadoHorarioEnum.LIBRE)
            )
    db.session.commit()
    return canchas


def _crear_reservas_demo(usuarios, canchas):
    deportista = usuarios[RolEnum.DEPORTISTA]
    hoy = date.today()

    reserva_confirmada = Reserva(
        usuario_id=deportista.id,
        cancha_id=canchas[0].id,
        fecha=hoy + timedelta(days=1),
        hora=time(hour=10),
        monto=canchas[0].precio,
        estado=EstadoReservaEnum.CONFIRMADA,
    )
    reserva_pendiente = Reserva(
        usuario_id=deportista.id,
        cancha_id=canchas[1].id,
        fecha=hoy + timedelta(days=2),
        hora=time(hour=15),
        monto=canchas[1].precio,
        estado=EstadoReservaEnum.PENDIENTE_PAGO,
    )
    db.session.add_all([reserva_confirmada, reserva_pendiente])
    db.session.commit()

    db.session.add_all(
        [
            OrdenPago(
                reserva_id=reserva_confirmada.id,
                monto=reserva_confirmada.monto,
                estado_pago=EstadoPagoEnum.APROBADO,
            ),
            OrdenPago(
                reserva_id=reserva_pendiente.id,
                monto=reserva_pendiente.monto,
                estado_pago=EstadoPagoEnum.PENDIENTE,
            ),
        ]
    )
    db.session.commit()


def sembrar_datos():
    if Usuario.query.first():
        print("La base de datos ya contiene información. Seed cancelado.")
        return

    usuarios = _crear_usuarios()
    canchas = _crear_canchas()
    _crear_reservas_demo(usuarios, canchas)

    print("Seed completado:")
    print(f"  - {len(usuarios)} usuarios demo (contraseña: {CONTRASENA_DEMO})")
    print(f"  - {len(canchas)} canchas con horarios de {HORA_INICIO_JORNADA}:00 a {HORA_FIN_JORNADA}:00")
    print("  - 2 reservas demo (1 confirmada, 1 pendiente de pago)")
