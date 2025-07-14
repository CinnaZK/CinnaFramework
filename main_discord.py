import logging
from dotenv import load_dotenv

from interfaces.discord import DiscordAgent


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """
    Entry point for the Heuman Agent Framework.
    Runs the Discord agent.
    """
    try:
        load_dotenv()

        logger.info("Starting Discord agent...")
        discord_agent = DiscordAgent()
        discord_agent.run()

    except KeyboardInterrupt:
        logger.info("Application stopped by user.")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise


if __name__ == "__main__":
    main()
