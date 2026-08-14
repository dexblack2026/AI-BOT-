import logging

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)


logger = logging.getLogger("TelegramBot")


class TelegramBot:

    def __init__(self, token: str):

        self.token = token

        self.app = (
            ApplicationBuilder()
            .token(token)
            .build()
        )

        # ==========================================
        # COMMANDS
        # ==========================================

        self.app.add_handler(
            CommandHandler(
                "start",
                self.start_command
            )
        )

        self.app.add_handler(
            CommandHandler(
                "predict",
                self.predict_command
            )
        )

        self.app.add_handler(
            CommandHandler(
                "stats",
                self.stats_command
            )
        )

        self.app.add_handler(
            CommandHandler(
                "history",
                self.history_command
            )
        )

        # ==========================================
        # BUTTONS
        # ==========================================

        self.app.add_handler(
            CallbackQueryHandler(
                self.button_handler
            )
        )

    # =================================================
    # MAIN KEYBOARD
    # =================================================

    def main_keyboard(self):

        keyboard = [

            [
                InlineKeyboardButton(
                    "🔮 PREDICT",
                    callback_data="predict"
                ),

                InlineKeyboardButton(
                    "📊 STATS",
                    callback_data="stats"
                ),
            ],

            [
                InlineKeyboardButton(
                    "🧬 PATTERN",
                    callback_data="pattern"
                ),

                InlineKeyboardButton(
                    "📚 HISTORY",
                    callback_data="history"
                ),
            ],

            [
                InlineKeyboardButton(
                    "🧠 LEARNING",
                    callback_data="learning"
                ),

                InlineKeyboardButton(
                    "⚙️ ENGINE",
                    callback_data="engine"
                ),
            ],

        ]

        return InlineKeyboardMarkup(keyboard)

    # =================================================
    # /START
    # =================================================

    async def start_command(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):

        text = (
            "╔══════════════════════════════╗\n"
            "║     🤖 <b>AI PREDICTION</b>      ║\n"
            "║        <b>ENGINE</b>             ║\n"
            "╚══════════════════════════════╝\n\n"

            "🚀 <b>System Online</b>\n\n"

            "🔎 Similar Search     <b>ONLINE</b>\n"
            "🧬 Pattern Mining     <b>ONLINE</b>\n"
            "🧪 Backtesting        <b>ONLINE</b>\n"
            "📚 Evidence           <b>ONLINE</b>\n"
            "🧠 Memory             <b>ONLINE</b>\n"
            "⚡ Learning           <b>ONLINE</b>\n"
            "🔮 Prediction         <b>ONLINE</b>\n\n"

            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

            "📌 <b>Analysis Pipeline</b>\n\n"

            "Historical Data\n"
            "      ↓\n"
            "Similar Sequence Search\n"
            "      ↓\n"
            "Pattern Mining\n"
            "      ↓\n"
            "Backtesting\n"
            "      ↓\n"
            "Evidence Check\n"
            "      ↓\n"
            "Formula Fallback\n"
            "      ↓\n"
            "Prediction\n\n"

            "👇 <b>ရွေးချယ်ပါ</b>"
        )

        await update.message.reply_text(
            text,
            parse_mode="HTML",
            reply_markup=self.main_keyboard(),
        )

    # =================================================
    # /PREDICT
    # =================================================

    async def predict_command(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):

        text = self.prediction_screen()

        await update.message.reply_text(
            text,
            parse_mode="HTML",
            reply_markup=self.main_keyboard(),
        )

    # =================================================
    # /STATS
    # =================================================

    async def stats_command(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):

        text = (
            "╔══════════════════════════════╗\n"
            "║       📊 <b>STATISTICS</b>       ║\n"
            "╚══════════════════════════════╝\n\n"

            "🎮 Total Analysis : <code>0</code>\n"
            "✅ Correct        : <code>0</code>\n"
            "❌ Wrong          : <code>0</code>\n"
            "📈 Accuracy       : <code>0.00%</code>\n\n"

            "🧬 Pattern Hits   : <code>0</code>\n"
            "🧪 Backtest       : <code>0</code>\n"
            "🧠 Learned Rules  : <code>0</code>"
        )

        await update.message.reply_text(
            text,
            parse_mode="HTML",
            reply_markup=self.main_keyboard(),
        )

    # =================================================
    # /HISTORY
    # =================================================

    async def history_command(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):

        text = (
            "╔══════════════════════════════╗\n"
            "║       📚 <b>HISTORY</b>          ║\n"
            "╚══════════════════════════════╝\n\n"

            "📥 Historical data ကို\n"
            "API Engine ကနေ ရယူပြီး\n"
            "Search Engine ထဲ ပို့ပါမယ်။\n\n"

            "Status: 🟢 READY"
        )

        await update.message.reply_text(
            text,
            parse_mode="HTML",
            reply_markup=self.main_keyboard(),
        )

    # =================================================
    # PREDICTION SCREEN
    # =================================================

    def prediction_screen(self):

        return (
            "╔══════════════════════════════╗\n"
            "║      🔮 <b>PREDICTION</b>        ║\n"
            "╚══════════════════════════════╝\n\n"

            "🎯 Target Issue\n"
            "   <code>WAITING...</code>\n\n"

            "🔮 Prediction\n"
            "   <b>WAITING...</b>\n\n"

            "🧬 Method\n"
            "   <code>WAITING...</code>\n\n"

            "🔍 Pattern\n"
            "   <code>WAITING...</code>\n\n"

            "🔢 Historical Matches\n"
            "   <code>0</code>\n\n"

            "🧪 Backtest\n"
            "   <code>0.00%</code>\n\n"

            "🧠 Evidence\n"
            "   <code>WAITING...</code>\n\n"

            "⚡ Status: <b>ENGINE READY</b>"
        )

    # =================================================
    # BUTTON HANDLER
    # =================================================

    async def button_handler(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):

        query = update.callback_query

        await query.answer()

        action = query.data

        # ---------------------------------------------
        # Prediction
        # ---------------------------------------------

        if action == "predict":

            await query.message.reply_text(
                self.prediction_screen(),
                parse_mode="HTML",
                reply_markup=self.main_keyboard(),
            )

        # ---------------------------------------------
        # Stats
        # ---------------------------------------------

        elif action == "stats":

            await query.message.reply_text(
                "📊 <b>Statistics Engine</b>\n\n"
                "Status: 🟢 ONLINE",
                parse_mode="HTML",
                reply_markup=self.main_keyboard(),
            )

        # ---------------------------------------------
        # Pattern
        # ---------------------------------------------

        elif action == "pattern":

            await query.message.reply_text(
                "🧬 <b>Pattern Mining</b>\n\n"
                "Historical sequence search "
                "engine is ready.",
                parse_mode="HTML",
                reply_markup=self.main_keyboard(),
            )

        # ---------------------------------------------
        # History
        # ---------------------------------------------

        elif action == "history":

            await query.message.reply_text(
                "📚 <b>Historical Data</b>\n\n"
                "API → History → Search Engine",
                parse_mode="HTML",
                reply_markup=self.main_keyboard(),
            )

        # ---------------------------------------------
        # Learning
        # ---------------------------------------------

        elif action == "learning":

            await query.message.reply_text(
                "🧠 <b>Learning Engine</b>\n\n"
                "Memory and backtest learning "
                "will be connected next.",
                parse_mode="HTML",
                reply_markup=self.main_keyboard(),
            )

        # ---------------------------------------------
        # Engine
        # ---------------------------------------------

        elif action == "engine":

            await query.message.reply_text(
                "⚙️ <b>ENGINE STATUS</b>\n\n"
                "🔎 Search       🟢\n"
                "🧬 Pattern      🟢\n"
                "🧪 Backtest     🟢\n"
                "📚 Evidence     🟢\n"
                "🧠 Memory       🟢\n"
                "⚡ Learning     🟢\n"
                "🔮 Prediction   🟢",
                parse_mode="HTML",
                reply_markup=self.main_keyboard(),
            )

    # =================================================
    # START BOT
    # =================================================

    async def start(self):

        logger.info(
            "Starting Telegram Bot..."
        )

        await self.app.initialize()

        await self.app.start()

        await self.app.updater.start_polling()

        logger.info(
            "✅ Telegram Bot is running."
        )

        # Keep application alive
        try:

            while True:

                await __import__("asyncio").sleep(3600)

        finally:

            await self.app.updater.stop()

            await self.app.stop()

            await self.app.shutdown()
