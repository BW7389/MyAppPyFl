class Config:
    """Configuration for Flask application."""
    @staticmethod
    def init_app(app):
        app.config.from_prefixed_env()