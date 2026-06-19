from app.auth.services import registrar_usuario, autenticar_usuario, CredencialesInvalidasError
from app.models.usuario import RolEnum


def test_registro_y_login_exitoso(app):
    registrar_usuario("Juan Pérez", "juan@test.com", "0411111111", RolEnum.DEPORTISTA, "Clave123*")
    usuario = autenticar_usuario("juan@test.com", "Clave123*")
    assert usuario.email == "juan@test.com"


def test_login_con_clave_incorrecta_lanza_error(app):
    registrar_usuario("Ana López", "ana@test.com", "0422222222", RolEnum.DEPORTISTA, "Clave123*")
    try:
        autenticar_usuario("ana@test.com", "incorrecta")
        assert False, "Debía lanzar CredencialesInvalidasError"
    except CredencialesInvalidasError:
        pass
