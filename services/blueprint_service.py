class BlueprintService:
    """Handles registration of all blueprints."""
    def __init__(self, blueprints):
        self.blueprints = blueprints

    def register_blueprints(self, app):
        """Register blueprints with specific URL prefixes."""
        for blueprint, url_prefix in self.blueprints:
            app.register_blueprint(blueprint, url_prefix=url_prefix)