"""
Main Flask Application Entry Point
"""
import logging
from flask import Flask
from flask_cors import CORS
from config.config import Config
from app.application.di_container import DIContainer
from app.presentation.routes import create_routes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app():
    """Application factory pattern"""
    # Load configuration
    config = Config.get_config()
    
    # Create Flask app
    app = Flask(__name__)
    app.config["SECRET_KEY"] = config.app.SECRET_KEY
    app.config["DEBUG"] = config.app.DEBUG
    
    # Enable CORS
    CORS(app, origins=config.api.CORS_ORIGINS)
    
    # Initialize dependency injection container
    di_container = DIContainer(config.nlp)
    
    # Register routes
    routes_bp = create_routes(di_container)
    app.register_blueprint(routes_bp, url_prefix=config.api.API_PREFIX)
    
    logger.info(f"Flask app created - Environment: {config.app.FLASK_ENV}")
    logger.info(f"API available at {config.api.API_PREFIX}")
    
    return app


if __name__ == "__main__":
    app = create_app()
    config = Config.get_config()
    app.run(
        host=config.app.HOST,
        port=config.app.PORT,
        debug=config.app.DEBUG,
    )
