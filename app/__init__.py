"""
StudySync AI Flask application factory.
"""
import os
from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics
from .logger import setup_root_logger, get_logger

logger = get_logger(__name__)


def create_app() -> Flask:
    """
    Create and configure the Flask application.
    Returns the configured Flask app instance.
    """
    setup_root_logger()

    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("TRIGGER_SECRET_TOKEN", "dev-secret-unsafe")

    # Initialize Prometheus metrics — this adds /metrics endpoint automatically
    metrics = PrometheusMetrics(app)
    metrics.info("studysync_app_info", "StudySync AI application info", version="1.0.0")

    # Register routes
    from app.routes import bp
    app.register_blueprint(bp)

    logger.info(
        "StudySync AI application started",
        extra={
            "flask_env": os.getenv("FLASK_ENV", "development"),
            "scheduler_hour": os.getenv("SCHEDULER_HOUR", "8"),
            "trigger_keywords": os.getenv("TRIGGER_KEYWORDS", "exam,test,ca"),
        }
    )

    return app
