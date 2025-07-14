import logging
from dotenv import load_dotenv

from interfaces.api import FlaskAgent


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """
    Entry point for the Heuman Agent Framework.
    Runs the Flask API agent.
    WARNING: This is not intended for production environments.
    """
    try:
        load_dotenv()

        logger.info("Starting Flask API agent...")
        flask_agent = FlaskAgent()
        flask_agent.run(host="0.0.0.0", port=5005)

    except KeyboardInterrupt:
        logger.info("Application stopped by user.")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise


if __name__ == "__main__":
    main()
