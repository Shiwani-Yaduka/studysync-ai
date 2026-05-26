"""
StudySync AI — Application entry point.
Run with: python run.py
"""
import os
import signal
import sys

# Load .env file in development (python-dotenv)
# In production (Docker/k3s), environment variables are injected by Kubernetes
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not available — relying on real environment variables

from app import create_app
from app.scheduler import start_scheduler, stop_scheduler
from app.logger import get_logger

logger = get_logger(__name__)


def handle_shutdown(signum, frame):
    """Handle graceful shutdown on SIGTERM/SIGINT."""
    logger.info("Shutdown signal received — stopping scheduler")
    stop_scheduler()
    sys.exit(0)


if __name__ == "__main__":
    # Register shutdown handlers
    signal.signal(signal.SIGTERM, handle_shutdown)
    signal.signal(signal.SIGINT, handle_shutdown)

    app = create_app()

    # Start the background scheduler
    start_scheduler(app)

    port = int(os.getenv("FLASK_PORT", "5000"))
    debug = os.getenv("FLASK_ENV", "production") == "development"

    logger.info("Starting StudySync AI server", extra={"port": port, "debug": debug})

    # Use threaded=True so scheduler and Flask run concurrently
    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug,
        use_reloader=False,  # CRITICAL: reloader would start duplicate schedulers
        threaded=True
    )
