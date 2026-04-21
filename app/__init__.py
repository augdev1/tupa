from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicializa extensões
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    
    # Registra blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    return app

from app import models
