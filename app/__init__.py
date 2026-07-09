from flask import Flask

from app.config import Config


def create_app():
    """
    Application Factory for MedScribe AI.
    """

    app = Flask(__name__)

    app.secret_key = "medscribe_ai_secret"

    # Load configuration
    app.config.from_object(Config)

    # Register blueprints
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    return app