from flask import Flask
from config import Config
from services.database_service import DatabaseService
from services.jwt_service import JWTService
from services.blueprint_service import BlueprintService
from shell_context import make_shell_context 

# Import extensions
from extensions import db, migrate, jwt

# Import blueprints
from controllers.auth import auth_bp
from controllers.users import user_bp

def create_app():
    """Application factory function to create the Flask app."""
    
    app = Flask(__name__)

    # Load configuration
    Config.init_app(app)

    # Initialize services
    database_service = DatabaseService(db, migrate)
    jwt_service = JWTService(jwt)
    blueprint_service = BlueprintService([
        (auth_bp, '/auth'),
        (user_bp, '/users')
    ])

    # Initialize services with the app
    database_service.init_app(app)
    jwt_service.init_app(app)
    blueprint_service.register_blueprints(app)

    # Create all tables in the database
    database_service.create_all_tables(app)

    # Provide shell context for Flask CLI
    app.shell_context_processor(make_shell_context)

    return app