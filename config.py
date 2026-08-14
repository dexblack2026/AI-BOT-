# =========================================================
# AI-BOT CONFIGURATION
# SC 60s GAME
# =========================================================

# =========================================================
# TELEGRAM
# =========================================================

TELEGRAM_BOT_TOKEN = (
    "8910093120:AAEXKCBhY18J2zZ2rDTKvImFlWiWOuhDBJQ"
)


# =========================================================
# API AUTHORIZATION
# =========================================================
# Supabase / Website Authorization Bearer Token

AUTHORIZATION_TOKEN = (
    "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVc2VySWQiOiIzNmI0ZWNiZi1hNzMzLTQyNzctOTY5OC1iM2FmYmY5OTE1ZjAiLCJVc2VyTmFtZSI6Ijk3Nzg5MDUyMjAiLCJuYW1lIjoiTWVtYmVyUUs3WVZNUU8iLCJleHAiOjE3ODY3MjY3MTd9.uatfENIuYW4JzKAPRo5jvL-1W2Yv5M5s9sKbBHRbwhM"
)


# =========================================================
# GAME SETTINGS
# =========================================================

# SC = Game Time
GAME_TIME = 60

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
# API REQUEST
# =========================================================

REQUEST_TIMEOUT = 8

PAGE_SIZE = 500

PAGE_NUMBER = 1


# =========================================================
# HISTORY
# =========================================================

DATA_FILE = (
    "data/game_history.json"
)

MAX_HISTORY = 2000


# =========================================================
# PATTERN SEARCH
# =========================================================

MIN_HISTORY_MATCHES = 3

MIN_PATTERN_LENGTH = 3

MAX_PATTERN_LENGTH = 12


# =========================================================
# NUMBER RANGE
# =========================================================

MIN_NUMBER = 0

MAX_NUMBER = 9


# =========================================================
# BIG / SMALL
# =========================================================
# 0-4 = SMALL
# 5-9 = BIG

BIG_THRESHOLD = 5


# =========================================================
# FORMULA FALLBACK
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


# =========================================================
# PREDICTION
# =========================================================

MIN_CONFIDENCE = 50.0


# =========================================================
# LOGGING
# =========================================================

LOG_LEVEL = "INFO"


# =========================================================
# VALIDATION
# =========================================================

def validate_config():

    if not TELEGRAM_BOT_TOKEN:
        raise ValueError(
            "TELEGRAM_BOT_TOKEN is missing."
        )

    if not AUTHORIZATION_TOKEN:
        raise ValueError(
            "AUTHORIZATION_TOKEN is missing."
        )

    if GAME_TIME <= 0:
        raise ValueError(
            "GAME_TIME must be greater than 0."
        )

    if CHECK_INTERVAL <= 0:
        raise ValueError(
            "CHECK_INTERVAL must be greater than 0."
        )

    if MIN_NUMBER < 0:
        raise ValueError(
            "MIN_NUMBER is invalid."
        )

    if MAX_NUMBER > 9:
        raise ValueError(
            "MAX_NUMBER is invalid."
        )

    if MIN_PATTERN_LENGTH < 1:
        raise ValueError(
            "MIN_PATTERN_LENGTH is invalid."
        )

    if MAX_PATTERN_LENGTH < MIN_PATTERN_LENGTH:
        raise ValueError(
            "MAX_PATTERN_LENGTH is invalid."
        )
