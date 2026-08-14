# =========================================================
# AI-BOT - TELEGRAM BOT
# =========================================================

import asyncio
import logging
from typing import Optional

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from prediction_engine import PredictionEngine


logger = logging.getLogger("TelegramBot")


class TelegramBot:

    # =====================================================
    # INIT
    # =====================================================

    def __init__(
        self,
        token: str,
        api,
        pattern_engine,
        formula_engine,
        backtest_engine,
        evidence_engine,
        memory_engine,
        learning_engine,
        game_seconds: int = 60,
        check_interval: int = 3,
    ):

        self.token = token

        self.api = api
        self.pattern_engine = pattern_engine
        self.formula_engine = formula_engine
        self.backtest_engine = backtest_engine
        self.evidence_engine = evidence_engine
        self.memory_engine = memory_engine
        self.learning_engine = learning_engine

        self.game_seconds = game_seconds
        self.check_interval = check_interval

        self.prediction_engine = (
            PredictionEngine()
        )

        self.application: Optional[
            Application
        ] = None

        self.users = set()

        self.last_issue = None
        self.last_prediction = None

        self.running = False

        self.session_wins = 0
        self.session_losses = 0

    # =====================================================
    # START
    # =====================================================

    async def start_command(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):

        if update.effective_chat:

            self.users.add(
                update.effective_chat.id
            )

        await update.message.reply_text(
            "🤖 <b>AI Prediction Engine Active</b>\n\n"
            "🎮 SC : <b>60s</b>\n"
            "📡 Waiting for game data...\n"
            "🔮 Next Period prediction will "
            "appear automatically.",
            parse_mode="HTML",
        )

    # =====================================================
    # STATS
    # =====================================================

    async def stats_command(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):

        total = (
            self.session_wins
            + self.session_losses
        )

        accuracy = (
            self.session_wins
            / total
            * 100.0
            if total
            else 0.0
        )

        text = (
            "📊 <b>SESSION STATISTICS</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"🎮 Rounds : <code>{total}</code>\n"
            f"✅ Wins : <code>{self.session_wins}</code>\n"
            f"❌ Losses : <code>{self.session_losses}</code>\n"
            f"📈 Accuracy : <code>{accuracy:.2f}%</code>"
        )

        await update.message.reply_text(
            text,
            parse_mode="HTML",
        )

    # =====================================================
    # BUILD MESSAGE
    # =====================================================

    def build_prediction_message(
        self,
        result: dict,
    ) -> str:

        prediction = result.get(
            "prediction"
        )

        if prediction == "B":

            prediction_text = (
                "🔴 <b>BIG</b>"
            )

        elif prediction == "S":

            prediction_text = (
                "🔵 <b>SMALL</b>"
            )

        else:

            prediction_text = (
                "⚠️ <b>NO SIGNAL</b>"
            )

        next_period = result.get(
            "next_period"
        )

        confidence = result.get(
            "confidence",
            0.0,
        )

        method = result.get(
            "method",
            "NO_EVIDENCE",
        )

        status = result.get(
            "status",
            "UNKNOWN",
        )

        if status == "STRONG":

            status_text = (
                "🟢 <b>STRONG</b>"
            )

        elif status == "MODERATE":

            status_text = (
                "🟡 <b>MODERATE</b>"
            )

        elif status == "WEAK":

            status_text = (
                "🟠 <b>WEAK</b>"
            )

        else:

            status_text = (
                "⚪ <b>NO SIGNAL</b>"
            )

        return (
            "🤖 <b>AI PREDICTION</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"🎮 <b>SC : {self.game_seconds}s</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"🎯 <b>NEXT PERIOD</b>\n"
            f"<code>{next_period or 'N/A'}</code>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"🔮 <b>PREDICTION</b>\n"
            f"{prediction_text}\n\n"
            f"🧠 <b>CONFIDENCE</b>\n"
            f"<code>{confidence:.2f}%</code>\n\n"
            f"⚙️ <b>METHOD</b>\n"
            f"<code>{method}</code>\n\n"
            f"📊 <b>STATUS</b>\n"
            f"{status_text}\n"
            "━━━━━━━━━━━━━━━━━━━━"
        )

    # =====================================================
    # GET DATA
    # =====================================================

    async def get_data(self):

        try:

            # api.py ထဲမှာ ဒီ method ရှိရမယ်
            return await self.api.get_game_data()

        except Exception as error:

            logger.error(
                "API error: %s",
                error,
            )

            return None, []

    # =====================================================
    # PROCESS GAME
    # =====================================================

    async def process_game(
        self,
    ):

        current_period, history = (
            await self.get_data()
        )

        if not current_period:
            return

        if not history:
            return

        # -------------------------------------------------
        # Prevent duplicate prediction
        # -------------------------------------------------

        if (
            self.last_issue
            == current_period
        ):

            return

        # -------------------------------------------------
        # Actual previous result
        # -------------------------------------------------

        if (
            self.last_prediction
            and history
        ):

            actual = history[-1].get(
                "bs"
            )

            old_prediction = (
                self.last_prediction.get(
                    "prediction"
                )
            )

            evaluation = (
                self.learning_engine.evaluate(
                    old_prediction,
                    actual,
                )
            )

            if evaluation.get(
                "valid"
            ):

                if evaluation.get(
                    "correct"
                ):

                    self.session_wins += 1

                else:

                    self.session_losses += 1

                # -----------------------------------------
                # Learn
                # -----------------------------------------

                self.learning_engine.learn(

                    pattern=self.last_prediction.get(
                        "pattern"
                    ),

                    pattern_prediction=self.last_prediction.get(
                        "prediction"
                    ),

                    formula_key=self.last_prediction.get(
                        "formula_key"
                    ),

                    formula_prediction=self.last_prediction.get(
                        "formula_prediction"
                    ),

                    actual_result=actual,
                )

        # -------------------------------------------------
        # Pattern Engine
        # -------------------------------------------------

        try:

            pattern_result = (
                self.pattern_engine.analyze(
                    history
                )
            )

        except Exception as error:

            logger.error(
                "Pattern engine error: %s",
                error,
            )

            pattern_result = {}

        # -------------------------------------------------
        # Formula Engine
        # -------------------------------------------------

        try:

            formula_result = (
                self.formula_engine.analyze(
                    history
                )
            )

        except Exception as error:

            logger.error(
                "Formula engine error: %s",
                error,
            )

            formula_result = {}

        # -------------------------------------------------
        # Backtest
        # -------------------------------------------------

        try:

            backtest_result = (
                self.backtest_engine.run(
                    history,
                    getattr(
                        self.formula_engine,
                        "s_formula",
                        {},
                    ),
                    getattr(
                        self.formula_engine,
                        "b_formula",
                        {},
                    ),
                )
            )

        except Exception as error:

            logger.error(
                "Backtest engine error: %s",
                error,
            )

            backtest_result = {}

        # -------------------------------------------------
        # Evidence
        # -------------------------------------------------

        try:

            evidence = (
                self.evidence_engine.build(
                    pattern_result,
                    formula_result,
                    backtest_result,
                )
            )

        except Exception as error:

            logger.error(
                "Evidence engine error: %s",
                error,
            )

            evidence = {}

        # -------------------------------------------------
        # Pattern Memory
        # -------------------------------------------------

        pattern = None

        if pattern_result:

            pattern = (
                pattern_result.get(
                    "pattern"
                )
            )

        pattern_memory = {}

        if pattern:

            pattern_memory = (
                self.memory_engine.get_pattern(
                    pattern
                )
            )

        # -------------------------------------------------
        # Formula Memory
        # -------------------------------------------------

        formula_key = None

        if formula_result:

            formula_key = (
                formula_result.get(
                    "rule_key"
                )
            )

        formula_memory = {}

        if formula_key:

            formula_memory = (
                self.memory_engine.get_formula(
                    formula_key
                )
            )

        # -------------------------------------------------
        # Final Prediction
        # -------------------------------------------------

        result = (
            self.prediction_engine.predict(

                current_period=current_period,

                evidence=evidence,

                pattern_memory=pattern_memory,

                formula_memory=formula_memory,

                pattern=pattern,

                formula_key=formula_key,
            )
        )

        # -------------------------------------------------
        # Save current prediction
        # -------------------------------------------------

        self.last_issue = (
            current_period
        )

        self.last_prediction = {

            "period":
                result.get(
                    "next_period"
                ),

            "prediction":
                result.get(
                    "prediction"
                ),

            "pattern":
                pattern,

            "formula_key":
                formula_key,

            "formula_prediction":
                (
                    formula_result.get(
                        "prediction"
                    )
                    if formula_result
                    else None
                ),

        }

        # -------------------------------------------------
        # Telegram message
        # -------------------------------------------------

        message = (
            self.build_prediction_message(
                result
            )
        )

        await self.broadcast(
            message
        )

    # =====================================================
    # BROADCAST
    # =====================================================

    async def broadcast(
        self,
        message: str,
    ):

        if not self.application:
            return

        for chat_id in list(
            self.users
        ):

            try:

                await self.application.bot.send_message(
                    chat_id=chat_id,
                    text=message,
                    parse_mode="HTML",
                )

            except Exception as error:

                logger.error(
                    "Telegram send error %s: %s",
                    chat_id,
                    error,
                )

    # =====================================================
    # AUTO LOOP
    # =====================================================

    async def auto_loop(
        self,
    ):

        self.running = True

        while self.running:

            try:

                await self.process_game()

            except Exception as error:

                logger.exception(
                    "Auto loop error: %s",
                    error,
                )

            await asyncio.sleep(
                self.check_interval
            )

    # =====================================================
    # POST INIT
    # =====================================================

    async def post_init(
        self,
        application: Application,
    ):

        self.application = (
            application
        )

        asyncio.create_task(
            self.auto_loop()
        )

    # =====================================================
    # RUN
    # =====================================================

    def run(
        self,
    ):

        application = (
            Application.builder()
            .token(self.token)
            .post_init(self.post_init)
            .build()
        )

        self.application = (
            application
        )

        application.add_handler(
            CommandHandler(
                "start",
                self.start_command,
            )
        )

        application.add_handler(
            CommandHandler(
                "stats",
                self.stats_command,
            )
        )

        logger.info(
            "Telegram bot started"
        )

        application.run_polling()
