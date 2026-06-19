from functools import wraps
from flask import abort
from flask_login import current_user
from app.utils.permissions import tiene_permiso


def roles_requeridos(*roles):
    def decorador(f):
        @wraps(f)
        def envoltura(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if current_user.rol not in roles:
                abort(403)
            return f(*args, **kwargs)
        return envoltura
    return decorador


def permiso_requerido(permiso):
    def decorador(f):
        @wraps(f)
        def envoltura(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if not tiene_permiso(current_user, permiso):
                abort(403)
            return f(*args, **kwargs)
        return envoltura
    return decorador
