import logging
from dotenv import load_dotenv

from agents.core_agent import CoreAgent
from interfaces.telegram import TelegramAgent


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def run_telegram(agent: TelegramAgent):
    """Run the Telegram agent."""
    try:
        logger.info("Starting Telegram agent...")
        agent.run()
    except Exception as e:
        logger.error(f"Telegram agent error: {e}")


def main():
    """
    Entry point for the Heuman Agent Framework.
    """
    try:
        # Load environment variables
        load_dotenv()

        # Instantiate shared CoreAgent
        core_agent = CoreAgent()
        telegram_agent = TelegramAgent(core_agent)

        # Run Telegram integration
        run_telegram(telegram_agent)

    except KeyboardInterrupt:
        logger.info("Application stopped by user.")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise


if __name__ == "__main__":
    main()
