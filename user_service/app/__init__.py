from flask import Flask
from .routes import user_bp, api

def create_app():
    app = Flask(__name__)
    app.register_blueprint(user_bp, url_prefix='/api/users')
    api.init_app(app)
    return app
