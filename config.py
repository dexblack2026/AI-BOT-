# =========================================================
# AI-BOT - CONFIGURATION
# =========================================================

import os


# =========================================================
# TELEGRAM BOT
# =========================================================

# @BotFather မှရတဲ့ Telegram Bot Token
#
# VPS မှာ environment variable သုံးနိုင်ပါတယ်။
# မထည့်ထားရင် placeholder ကို အသုံးပြုပါမယ်။

TELEGRAM_BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN",
    "8910093120:AAEXKCBhY18J2zZ2rDTKvImFlWiWOuhDBJQ"
)


# =========================================================
# API AUTHORIZATION
# =========================================================

# မူရင်း code မှာ အသုံးပြုထားတဲ့
# Supabase Authorization Bearer Token
#
# VPS environment variable:
#
# export AUTHORIZATION_TOKEN="Bearer YOUR_TOKEN"
#
# လုပ်ထားနိုင်ပါတယ်။

AUTHORIZATION_TOKEN = os.getenv(
    "AUTHORIZATION_TOKEN",
    "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVc2VySWQiOiIzNmI0ZWNiZi1hNzMzLTQyNzctOTY5OC1iM2FmYmY5OTE1ZjAiLCJVc2VyTmFtZSI6Ijk3Nzg5MDUyMjAiLCJuYW1lIjoiTWVtYmVyUUs3WVZNUU8iLCJleHAiOjE3ODY3MjY3MTd9.uatfENIuYW4JzKAPRo5jvL-1W2Yv5M5s9sKbBHRbwhM"
)


# =========================================================
# GAME
# =========================================================

# SC Game Time
GAME_SECONDS = 60

# API polling interval
CHECK_INTERVAL = 3


# =========================================================
# API URL
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
# API HEADERS
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

API_TIMEOUT = 8

HISTORY_PAGE_SIZE = 500

HISTORY_PAGE_NUMBER = 1


# =========================================================
# DATA
# =========================================================

DATA_DIR = "data"

DATA_FILE = os.path.join(
    DATA_DIR,
    "game_history.json"
)


# =========================================================
# MEMORY
# =========================================================

MODELS_DIR = "models"

PATTERN_MEMORY_FILE = os.path.join(
    MODELS_DIR,
    "pattern_memory.json"
)

FORMULA_MEMORY_FILE = os.path.join(
    MODELS_DIR,
    "formula_memory.json"
)


# =========================================================
# HISTORY LIMIT
# =========================================================

MAX_HISTORY_ITEMS = 2000


# =========================================================
# PATTERN SETTINGS
# =========================================================

MIN_HISTORY_MATCHES = 3

MIN_PATTERN_LENGTH = 3

MAX_PATTERN_LENGTH = 12


# =========================================================
# CONFIDENCE
# =========================================================

MIN_CONFIDENCE = 50.0

STRONG_CONFIDENCE = 70.0


# =========================================================
# MEMORY SETTINGS
# =========================================================

MEMORY_MIN_SAMPLES = 3

MEMORY_MAX_ENTRIES = 5000


# =========================================================
# LEARNING
# =========================================================

LEARNING_ENABLED = True

LEARN_ONLY_VALID_RESULTS = True


# =========================================================
# LOGGING
# =========================================================

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)


# =========================================================
# CREATE DIRECTORIES
# =========================================================

os.makedirs(
    DATA_DIR,
    exist_ok=True
)

os.makedirs(
    MODELS_DIR,
    exist_ok=True
)
