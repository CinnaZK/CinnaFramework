import asyncio
import logging
from dotenv import load_dotenv

from interfaces.farcaster_reply import FarcasterReplyAgent


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    """
    Entry point for the Heuman Agent Framework.
    Runs the Farcaster Reply agent for automated replies.
    """
    try:
        load_dotenv()

        logger.info("Starting Farcaster Reply agent...")
        farcaster_agent = FarcasterReplyAgent()
        await farcaster_agent.start()

    except KeyboardInterrupt:
        logger.info("Application stopped by user.")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
