from flask import jsonify
from flask_jwt_extended import JWTManager

class JWTService:
    """Handles JWT setup and error handlers."""
    def __init__(self, jwt):
        self.jwt = jwt

    def init_app(self, app):
        """Initialize JWT with app and setup error handlers."""
        self.jwt.init_app(app)
        self._register_error_handlers(app)

    def _register_error_handlers(self, app):
        """Register JWT error handlers."""
        @self.jwt.expired_token_loader
        def expired_token_callback(jwt_header, jwt_data):
            return jsonify({
                'message': 'The token has expired',
                'error': 'token_expired'
            }), 401

        @self.jwt.invalid_token_loader
        def invalid_token_callback(error):
            return jsonify({
                'message': 'Signature verification failed',
                'error': 'invalid_token'
            }), 401

        @self.jwt.unauthorized_loader
        def missing_token_callback(error):
            return jsonify({
                'message': 'Request does not contain an access token',
                'error': 'authorization_header_missing'
            }), 401