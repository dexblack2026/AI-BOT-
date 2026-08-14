# =========================================================
# AI-BOT CONFIG
# =========================================================

from pathlib import Path


# =========================================================
# PROJECT PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

MODELS_DIR = BASE_DIR / "models"


DATA_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

MODELS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# =========================================================
# TELEGRAM
# =========================================================

TELEGRAM_BOT_TOKEN = (
    "YOUR_TELEGRAM_BOT_TOKEN_HERE"
)


# =========================================================
# GAME API AUTH
# =========================================================

AUTHORIZATION_TOKEN = (
    "Bearer YOUR_JWT_TOKEN_HERE"
)


# =========================================================
# GAME API
# =========================================================

ISSUE_API_URL = (
    "https://qzgijlgwqxjwzlwctbke.supabase.co/"
    "functions/v1/get-game-issue"
)

HISTORY_API_URL = (
    "https://qzgijlgwqxjwzlwctbke.supabase.co/"
    "functions/v1/get-game-history"
)


# =========================================================
# HTTP HEADERS
# =========================================================

HEADERS = {

    "accept": "*/*",

    "accept-language":
        "en-US,en;q=0.9",

    "authorization":
        AUTHORIZATION_TOKEN,

    "content-type":
        "application/json",

    "origin":
        "https://mini-game.site",

    "referer":
        "https://mini-game.site/",

    "user-agent":
        (
            "Mozilla/5.0 "
            "(Linux; Android 10; K) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/150.0.0.0 "
            "Mobile Safari/537.36"
        ),
}


# =========================================================
# API REQUEST
# =========================================================

REQUEST_TIMEOUT = 8

CHECK_INTERVAL = 3

PAGE_SIZE = 500

PAGE_NUMBER = 1


# =========================================================
# NUMBER RULE
# =========================================================

MIN_NUMBER = 0

MAX_NUMBER = 9

BIG_MIN_NUMBER = 5


# =========================================================
# HISTORY
# =========================================================

HISTORY_FILE = (
    DATA_DIR / "game_history.json"
)

MAX_HISTORY = 2000


# =========================================================
# SEARCH
# =========================================================

MIN_PATTERN_LENGTH = 3

MAX_PATTERN_LENGTH = 12

MIN_HISTORY_MATCHES = 3


# =========================================================
# BACKTEST
# =========================================================

BACKTEST_LOOKBACK = 500

BACKTEST_MIN_SAMPLES = 10


# =========================================================
# PREDICTION
# =========================================================

MIN_CONFIDENCE = 50.0

HIGH_CONFIDENCE = 75.0


# =========================================================
# MEMORY
# =========================================================

PATTERN_MEMORY_FILE = (
    MODELS_DIR /
    "pattern_memory.json"
)

FORMULA_MEMORY_FILE = (
    MODELS_DIR /
    "formula_memory.json"
)


# =========================================================
# GAME DISPLAY
# =========================================================

SHOW_TIME = True

SHOW_CURRENT_PERIOD = True

SHOW_NET_PERIOD = True

SHOW_NUMBER = True

SHOW_BS = True

SHOW_CONFIDENCE = True

SHOW_PATTERN = True

SHOW_BACKTEST = True

SHOW_EVIDENCE = True


# =========================================================
# LOGGING
# =========================================================

LOG_LEVEL = "INFO"

LOG_FILE = (
    BASE_DIR / "bot.log"
)
