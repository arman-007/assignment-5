from flask import Flask
from .routes import auth_bp, api

def create_app():
    app = Flask(__name__)
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    api.init_app(app)
    return app
