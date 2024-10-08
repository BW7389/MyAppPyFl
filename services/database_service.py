class DatabaseService:
    """Handles the initialization of the database and migrations."""
    def __init__(self, db, migrate):
        self.db = db
        self.migrate = migrate

    def init_app(self, app):
        """Initialize database and migrations."""
        self.db.init_app(app)
        self.migrate.init_app(app, self.db)

    def create_all_tables(self, app):
        """Create tables if they don't exist."""
        with app.app_context():
            self.db.create_all()