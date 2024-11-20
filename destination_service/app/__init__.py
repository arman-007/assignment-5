from flask import Flask
from .routes import destination_bp, api


def create_app():
    app = Flask(__name__)
    app.register_blueprint(destination_bp)
    api.init_app(app)
    return app