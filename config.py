# config.py

# =========================================================
# TELEGRAM
# =========================================================

TELEGRAM_BOT_TOKEN = (
    "YOUR_TELEGRAM_BOT_TOKEN_HERE"
)


# =========================================================
# API AUTH
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
    "accept-language": "en-US,en;q=0.9",
    "authorization": AUTHORIZATION_TOKEN,
    "content-type": "application/json",
    "origin": "https://mini-game.site",
    "referer": "https://mini-game.site/",
    "user-agent": (
        "Mozilla/5.0 "
        "(Linux; Android 10; K) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/150.0.0.0 "
        "Mobile Safari/537.36"
    ),
}


# =========================================================
# API SETTINGS
# =========================================================

REQUEST_TIMEOUT = 8

PAGE_SIZE = 500

PAGE_NUMBER = 1

CHECK_INTERVAL = 3


# =========================================================
# HISTORY STORAGE
# =========================================================

DATA_FILE = "data/game_history.json"

MAX_HISTORY = 2000


# =========================================================
# SEARCH SETTINGS
# =========================================================

MIN_PATTERN_LENGTH = 3

MAX_PATTERN_LENGTH = 12

MIN_HISTORY_MATCHES = 3


# =========================================================
# FORMULA SETTINGS
# =========================================================

S_FORMULA = {
    1: "B",
    2: "B",
    3: "S",
    4: "B",
    5: "S",
}

B_FORMULA = {
    1: "S",
    2: "S",
    3: "B",
    4: "S",
    5: "B",
    6: "S",
}


# =========================================================
# MEMORY
# =========================================================

PATTERN_MEMORY_FILE = (
    "models/pattern_memory.json"
)

FORMULA_MEMORY_FILE = (
    "models/formula_memory.json"
)
