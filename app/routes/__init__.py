from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    db.init_app(app)
    Migrate(app, db)

    # IMPORTA Y REGISTRA LAS RUTAS
    from app.routes.views import main
    app.register_blueprint(main)

    return app
