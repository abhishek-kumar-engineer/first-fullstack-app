# config.py
from dotenv import load_dotenv
import os

# .env file load karo
load_dotenv()

# ── Database ──────────────────────────────────────────
DB_CONFIG = {
    'host'    : os.getenv('DB_HOST', 'localhost'),
    'user'    : os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'first_fullstack_app')
}

# ── JWT ───────────────────────────────────────────────
JWT_SECRET  = os.getenv('JWT_SECRET')
JWT_EXPIRY  = int(os.getenv('JWT_EXPIRY', 24))

# AES key — exactly 32 characters hona chahiye (AES-256)
AES_SECRET_KEY    = os.getenv('AES_SECRET_KEY')
ENABLE_ENCRYPTION = os.getenv('ENABLE_ENCRYPTION', 'False') == 'True'

# ── Email Config ──────────────────────────────────────
MAIL_SERVER    = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT      = int(os.getenv('MAIL_PORT', 587))
MAIL_USE_TLS   = os.getenv('MAIL_USE_TLS', 'True') == 'True'
MAIL_USERNAME  = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD  = os.getenv('MAIL_PASSWORD')
MAIL_FROM_NAME = os.getenv('MAIL_FROM_NAME', 'First Fullstack App')

# ── Reset Token Config ───────────────────────────────────────
RESET_TOKEN_EXPIRY_MINUTES = int(os.getenv('RESET_TOKEN_EXPIRY_MINUTES', 15))
FRONTEND_URL               = os.getenv('FRONTEND_URL', 'http://localhost:4200')

# ── Flask ─────────────────────────────────────────────
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
