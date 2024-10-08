from flask import Flask
from extensions import db, migrate  # Import db and migrate from extensions
from shellContext import make_shell_context  # Import the function to create shell context

def create_app():
    # Create an instance of the Flask application
    app = Flask(__name__)

    # Load configuration from environment variables with a prefix
    app.config.from_prefixed_env()

    # Initialize the database (db) with the Flask application
    db.init_app(app)

    # Initialize Flask-Migrate with the application and database
    migrate.init_app(app, db)

    # Create an application context to use the db
    with app.app_context():
        # Create all tables in the database if they do not exist
        db.create_all()

    # Register shell context processor for easy access to db and User in the shell
    app.shell_context_processor(make_shell_context)

    # Return the instance of the Flask application
    return app
