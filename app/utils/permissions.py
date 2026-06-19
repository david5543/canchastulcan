from app.models.usuario import RolEnum

PERMISOS_POR_ROL = {
    RolEnum.ADMIN: {
        "usuarios:gestionar",
        "canchas:gestionar",
        "horarios:gestionar",
        "reservas:gestionar",
        "pagos:validar",
        "ocupaciones:gestionar",
        "reportes:ver",
        "notificaciones:gestionar",
    },
    RolEnum.DIRIGENTE: {
        "canchas:gestionar_asignadas",
        "horarios:gestionar_asignadas",
        "ocupaciones:gestionar",
        "reservas:consultar",
        "reportes:ver",
    },
    RolEnum.DEPORTISTA: {
        "reservas:crear",
        "reservas:cancelar",
        "reservas:consultar",
        "pagos:subir_comprobante",
    },
}


def tiene_permiso(usuario, permiso):
    if usuario is None or not usuario.is_authenticated:
        return False
    permisos = PERMISOS_POR_ROL.get(usuario.rol, set())
    return permiso in permisos
