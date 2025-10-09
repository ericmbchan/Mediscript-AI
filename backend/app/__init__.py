import os
from flask import Flask, send_from_directory
from flask_cors import CORS

from .routes import api_bp


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Load config
    app.config.from_object('app.config.Config')

    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')

    # API-only routes (no frontend)
    @app.route('/')
    def index():
        return {'message': 'Mediscript API is running', 'endpoints': ['/api/health', '/api/generate']}

    return app

