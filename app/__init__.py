import os
from flask import Flask
from app.config import config_by_name
from app.extensions import db, migrate, login_manager, bcrypt, csrf


def create_app(config_name=None):
    config_name = config_name or os.environ.get("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    _registrar_extensiones(app)
    _registrar_blueprints(app)
    _registrar_context_processors(app)
    _registrar_manejadores_error(app)
    _registrar_comandos_cli(app)

    return app


def _registrar_extensiones(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)

    from app.models.usuario import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Usuario, int(user_id))


def _registrar_blueprints(app):
    from app.auth.routes import auth_bp
    from app.dashboard.routes import dashboard_bp
    from app.usuarios.routes import usuarios_bp
    from app.canchas.routes import canchas_bp
    from app.reservas.routes import reservas_bp
    from app.pagos.routes import pagos_bp
    from app.ocupaciones.routes import ocupaciones_bp
    from app.reportes.routes import reportes_bp
    from app.notifications.routes import notifications_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(canchas_bp)
    app.register_blueprint(reservas_bp)
    app.register_blueprint(pagos_bp)
    app.register_blueprint(ocupaciones_bp)
    app.register_blueprint(reportes_bp)
    app.register_blueprint(notifications_bp)


def _registrar_context_processors(app):
    from flask_login import current_user
    from app.notifications.services import contar_no_leidas

    @app.context_processor
    def inyectar_globales():
        no_leidas = contar_no_leidas(current_user) if current_user.is_authenticated else 0
        return {"notificaciones_no_leidas": no_leidas}


def _registrar_manejadores_error(app):
    from flask import render_template

    @app.errorhandler(401)
    def no_autorizado(error):
        return render_template("errors/401.html"), 401

    @app.errorhandler(403)
    def prohibido(error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def no_encontrado(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def error_servidor(error):
        return render_template("errors/500.html"), 500


def _registrar_comandos_cli(app):
    @app.cli.command("seed-db")
    def seed_db():
        """Crea usuarios, canchas, horarios y reservas de demostración."""
        from app.seeds import sembrar_datos

        sembrar_datos()
