import logging
from dotenv import load_dotenv

from interfaces.farcaster_post import FarcasterAgent


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """
    Entry point for the Heuman Agent Framework.
    Runs the Farcaster agent for automated casting.
    """
    try:
        load_dotenv()

        logger.info("Starting Farcaster agent...")
        farcaster_agent = FarcasterAgent()
        farcaster_agent.run()

    except KeyboardInterrupt:
        logger.info("Application stopped by user.")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise


if __name__ == "__main__":
    main()
