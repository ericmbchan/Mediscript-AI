import os
from flask import Flask, send_from_directory

from .routes import api_bp


def create_app() -> Flask:
    app = Flask(
        __name__,
        static_folder='../../frontend',  # serve static assets from frontend directory
        static_url_path='',
    )

    # Load config
    app.config.from_object('app.config.Config')

    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')

    # Frontend routes
    @app.route('/')
    def index():
        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/<path:path>')
    def static_proxy(path: str):
        return send_from_directory(app.static_folder, path)

    return app

