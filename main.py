# =========================================================
# AI-BOT - MAIN
# =========================================================

import logging

from config import (
    TELEGRAM_BOT_TOKEN,
    GAME_SECONDS,
    CHECK_INTERVAL,
)

from api import GameAPI

from engine.search_engine import SearchEngine
from engine.pattern_engine import PatternEngine
from engine.formula_engine import FormulaEngine
from engine.backtest_engine import BacktestEngine
from engine.evidence_engine import EvidenceEngine
from engine.memory_engine import MemoryEngine
from engine.learning_engine import LearningEngine

from telegram_bot import TelegramBot


# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    ),
)

logger = logging.getLogger("Main")


# =========================================================
# BUILD ENGINE
# =========================================================

def build_bot():

    logger.info(
        "Initializing AI Prediction Engine..."
    )

    # -----------------------------------------------------
    # API
    # -----------------------------------------------------

    api = GameAPI()

    # -----------------------------------------------------
    # SEARCH ENGINE
    # -----------------------------------------------------

    search_engine = SearchEngine()

    # -----------------------------------------------------
    # PATTERN ENGINE
    # -----------------------------------------------------

    pattern_engine = PatternEngine(
        search_engine=search_engine,
    )

    # -----------------------------------------------------
    # FORMULA ENGINE
    # -----------------------------------------------------

    formula_engine = FormulaEngine()

    # -----------------------------------------------------
    # BACKTEST ENGINE
    # -----------------------------------------------------

    backtest_engine = BacktestEngine()

    # -----------------------------------------------------
    # EVIDENCE ENGINE
    # -----------------------------------------------------

    evidence_engine = EvidenceEngine()

    # -----------------------------------------------------
    # MEMORY ENGINE
    # -----------------------------------------------------

    memory_engine = MemoryEngine(
        pattern_file=(
            "models/pattern_memory.json"
        ),
        formula_file=(
            "models/formula_memory.json"
        ),
    )

    # -----------------------------------------------------
    # LEARNING ENGINE
    # -----------------------------------------------------

    learning_engine = LearningEngine(
        memory_engine=memory_engine,
    )

    # -----------------------------------------------------
    # TELEGRAM BOT
    # -----------------------------------------------------

    bot = TelegramBot(

        token=TELEGRAM_BOT_TOKEN,

        api=api,

        pattern_engine=pattern_engine,

        formula_engine=formula_engine,

        backtest_engine=backtest_engine,

        evidence_engine=evidence_engine,

        memory_engine=memory_engine,

        learning_engine=learning_engine,

        game_seconds=GAME_SECONDS,

        check_interval=CHECK_INTERVAL,
    )

    logger.info(
        "All engines initialized successfully."
    )

    return bot


# =========================================================
# MAIN
# =========================================================

def main():

    logger.info(
        "=========================================="
    )

    logger.info(
        "        AI PREDICTION BOT STARTING"
    )

    logger.info(
        "=========================================="
    )

    # -----------------------------------------------------
    # TOKEN CHECK
    # -----------------------------------------------------

    if not TELEGRAM_BOT_TOKEN:

        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN is not configured."
        )

    # -----------------------------------------------------
    # BUILD
    # -----------------------------------------------------

    bot = build_bot()

    # -----------------------------------------------------
    # RUN
    # -----------------------------------------------------

    try:

        bot.run()

    except KeyboardInterrupt:

        logger.info(
            "Bot stopped by user."
        )

    except Exception as error:

        logger.exception(
            "Fatal error: %s",
            error,
        )

        raise


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":

    main()
