from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Configuración de sesión
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Inicializar extensiones
    db.init_app(app)
    migrate = Migrate(app, db)

    # Importar modelos (evita errores de migraciones)
    from app.models import models

    # Importar y registrar blueprints DESPUÉS de crear la app
    from app.routes.views import main
    from app.routes.catalagos import catalagos

    app.register_blueprint(main)
    app.register_blueprint(catalagos, url_prefix="/admin/catalagos")

    return app
