from src.web.controllers.vehiculos import bp as vehiculos_bp
from src.web.controllers.usuarios import bp as usuarios_bp
from src.web.controllers.sucursales import bp as sucursales_bp
from src.web.controllers.inicio import bp as global_bp
from src.web.controllers.reservas import bp as reservas_bp
from src.web.controllers.auth import auth_bp  # Importar el blueprint de auth

def register_blueprints(app):
    app.register_blueprint(vehiculos_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(sucursales_bp)
    app.register_blueprint(global_bp)
    app.register_blueprint(reservas_bp)
    app.register_blueprint(auth_bp)  # Registrar el blueprint de auth
