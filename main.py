from flask import Flask, jsonify
from config import Config
from services.database_service import DatabaseService
from services.jwt_service import JWTService
from services.blueprint_service import BlueprintService
from shell_context import make_shell_context 
import mysql.connector
from mysql.connector import Error

# Import extensions
from extensions import db, migrate, jwt

# Import blueprints
from controllers.auth import auth_bp
from controllers.users import user_bp

from flask_swagger_ui import get_swaggerui_blueprint

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
    blueprint_service.register_blueprints(app)  # Register all blueprints

    # Swagger UI setup
    SWAGGER_URL = '/api/docs'  
    API_URL = '/static/swagger.yaml'  

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL, 
        API_URL,      
        config={     
            'app_name': "My API"
        }
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # Create all tables in the database
    database_service.create_all_tables(app)

    # Provide shell context for Flask CLI
    app.shell_context_processor(make_shell_context)

    @app.route('/health/db', methods=['GET'])
    def health_check():
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='letmein',
                database='flask_api_db',
                port=3307
            )
            if connection.is_connected():
                return jsonify({"status": "MySQL is running"}), 200
        except Error as e:
            return jsonify({"status": "MySQL is not running", "error": str(e)}), 500
        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()
                
    return app
