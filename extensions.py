from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



# Initialize the SQLAlchemy instance
db = SQLAlchemy()
migrate = Migrate()