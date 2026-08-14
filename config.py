# =========================================================
# AI-BOT - CONFIG.PY
# =========================================================

import os


# =========================================================
# TELEGRAM
# =========================================================

TELEGRAM_BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN",
    "8910093120:AAEXKCBhY18J2zZ2rDTKvImFlWiWOuhDBJQ"
)


# =========================================================
# API AUTHORIZATION
# =========================================================

AUTHORIZATION_TOKEN = os.getenv(
    "AUTHORIZATION_TOKEN",
    "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVc2VySWQiOiIzNmI0ZWNiZi1hNzMzLTQyNzctOTY5OC1iM2FmYmY5OTE1ZjAiLCJVc2VyTmFtZSI6Ijk3Nzg5MDUyMjAiLCJuYW1lIjoiTWVtYmVyUUs3WVZNUU8iLCJleHAiOjE3ODY3MjY3MTd9.uatfENIuYW4JzKAPRo5jvL-1W2Yv5M5s9sKbBHRbwhM"
)


# =========================================================
# GAME
# =========================================================

# SC = 60 seconds
GAME_SECONDS = 60

# API checking interval
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
# API REQUEST
# =========================================================

API_TIMEOUT = 8

PAGE_SIZE = 500

# IMPORTANT:
# api.py က PAGE_NUMBER ကို import လုပ်နေတာကြောင့်
# ဒီ variable name ကို PAGE_NUMBER လို့ပဲထားမယ်။

PAGE_NUMBER = 1


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
# HISTORY
# =========================================================

MAX_HISTORY_ITEMS = 2000


# =========================================================
# PATTERN
# =========================================================

MIN_HISTORY_MATCHES = 3

MIN_PATTERN_LENGTH = 3

MAX_PATTERN_LENGTH = 12


# =========================================================
# GAME RESULT
# =========================================================

BIG_THRESHOLD = 5


# =========================================================
# CONFIDENCE
# =========================================================

MIN_CONFIDENCE = 50.0

STRONG_CONFIDENCE = 70.0


# =========================================================
# MEMORY
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
