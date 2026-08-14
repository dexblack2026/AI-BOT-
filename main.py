import asyncio
import logging

from config import TELEGRAM_BOT_TOKEN
from telegram_bot import TelegramBot


# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("PredictionBot")


# =========================================================
# MAIN APPLICATION
# =========================================================

class Application:

    def __init__(self):

        self.telegram_bot = None

    # =====================================================
    # INITIALIZE
    # =====================================================

    def initialize(self):

        logger.info("===================================")
        logger.info("🤖 PREDICTION BOT INITIALIZING")
        logger.info("===================================")

        if not TELEGRAM_BOT_TOKEN:
            raise ValueError(
                "TELEGRAM_BOT_TOKEN is not configured."
            )

        # Telegram UI
        self.telegram_bot = TelegramBot(
            token=TELEGRAM_BOT_TOKEN
        )

        logger.info(
            "Telegram UI initialized."
        )

    # =====================================================
    # START
    # =====================================================

    async def start(self):

        self.initialize()

        logger.info(
            "🚀 Starting Telegram Prediction Bot..."
        )

        await self.telegram_bot.start()


# =========================================================
# ENTRY POINT
# =========================================================

def main():

    application = Application()

    try:

        asyncio.run(
            application.start()
        )

    except KeyboardInterrupt:

        logger.info(
            "🛑 Bot stopped."
        )

    except Exception as error:

        logger.exception(
            f"Fatal error: {error}"
        )


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    main()
