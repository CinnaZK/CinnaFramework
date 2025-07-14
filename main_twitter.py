import logging
from dotenv import load_dotenv

from agents.core_agent import CoreAgent
from interfaces.twitter_post import TwitterAgent


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """
    Entry point for the Heuman Agent Framework.
    Runs the Twitter agent for automated tweeting.
    """
    try:
        # Load environment variables
        load_dotenv()

        # Initialize and run Twitter agent
        logger.info("Starting Twitter agent...")
        core_agent = CoreAgent()
        twitter_agent = TwitterAgent(core_agent)
        twitter_agent.run()

    except KeyboardInterrupt:
        logger.info("Application stopped by user.")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise


if __name__ == "__main__":
    main()
