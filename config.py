"""
╔══════════════════════════════════════════════════════════════╗
║                         QUIZBOT — Configuration              ║
║                                                              ║
║  Sponsored by  : Qzio — qzio.in                              ║
║  Developed by  : devgagan — devgagan.in                      ║
╚══════════════════════════════════════════════════════════════╝

All sensitive values must be set via environment variables or
a `.env` file placed in the project root.  Never commit real
credentials to version control.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── Pyrogram (main.py bot) ────────────────────────────────────────────────────
API_ID    = int(os.getenv("API_ID", "21157244"))
API_HASH  = os.getenv("API_HASH", "4981c2699bd91c7db836ec8f77e5b0f0")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8284001698:AAHzl21WQIXqRWTjTPVHn3oPlNm72koC018")

# ── Telegram — secondary bot token used for HTML/API calls ───────────────────
BOT_TOKEN_2 = os.getenv("BOT_TOKEN_2", "8519255319:AAHiYDXU-N_KOdG4-OAajVWcQjZBeLzg268")

# ── MongoDB ───────────────────────────────────────────────────────────────────
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://saraswatisharmapbc:L8aRiWhBbhi8mFwN@cluster0.gxhxgye.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")          # Primary connection string
MONGO_URI_2 = os.getenv("MONGO_URI_2", "mongodb+srv://takkishor9784:gG73juoh44MnvJEZ@cluster0.q8hxdk2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")      # Secondary / replica connection
MONGO_URIX = os.getenv("MONGO_URIX", "")        # Quizzes async collection URI
DB_NAME   = os.getenv("DB_NAME", "quiz_bot")

# ── MySQL (Quizbot web panel) ───────────────────────────────────────
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_USER = os.getenv("MYSQL_USER", "")
MYSQL_PASS = os.getenv("MYSQL_PASS", "")
MYSQL_DB   = os.getenv("MYSQL_DB", "quizbot")

# ── Owner & Groups ────────────────────────────────────────────────────────────
OWNER_ID   = list(map(int, os.getenv("OWNER_ID", "1783306092").split()))
LOG_GROUP  = int(os.getenv("LOG_GROUP", "-1002758652479"))
FORCE_SUB  = int(os.getenv("FORCE_SUB", "-1002212409310"))
BOT_GROUP  = int(os.getenv("BOT_GROUP", "-1002212409310"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "-1002212409310"))

# ── Encryption ────────────────────────────────────────────────────────────────
MASTER_KEY = os.getenv("MASTER_KEY", "")
IV_KEY     = os.getenv("IV_KEY", "")

# ── Limits ────────────────────────────────────────────────────────────────────
FREEMIUM_LIMIT = int(os.getenv("FREEMIUM_LIMIT", "0"))
PREMIUM_LIMIT  = int(os.getenv("PREMIUM_LIMIT", "500"))

# ── Optional integrations ─────────────────────────────────────────────────────
PAY_API       = os.getenv("PAY_API", "")
YT_COOKIES    = os.getenv("YT_COOKIES", None)
INSTA_COOKIES = os.getenv("INSTA_COOKIES", None)
UMODE         = os.getenv("UMODE", None)

# ── Mode flags ────────────────────────────────────────────────────────────────
FREE_BOT = os.getenv("FREE_BOT", "true").lower() == "true"
