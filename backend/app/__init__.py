import os
from flask import Flask, send_from_directory

from .routes import api_bp


def create_app() -> Flask:
    app = Flask(__name__)

    # Load config
    app.config.from_object('app.config.Config')

    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')

    # API-only routes (no frontend)
    @app.route('/')
    def index():
        return {'message': 'Mediscript API is running', 'endpoints': ['/api/health', '/api/generate']}

    return app

