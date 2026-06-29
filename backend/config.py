# config.py
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',        # XAMPP mein default password blank hota hai
    'database': 'first_fullstack_app'
}

JWT_SECRET  = 'abhishek-super-secret-key-2026'  # strong key rakho
JWT_EXPIRY  = 24   # hours mein — token 24 ghante baad expire hoga

# AES key — exactly 32 characters hona chahiye (AES-256)
AES_SECRET_KEY = 'abhishek-aes-key-exactly-32chars'  # ← 32 chars count karo

ENABLE_ENCRYPTION = False

# ── Email Config ──────────────────────────────────────
MAIL_SERVER       = 'smtp.gmail.com'
MAIL_PORT         = 587
MAIL_USE_TLS      = True
MAIL_USERNAME     = 'abhishek.kumar.storage1@gmail.com'      # ← apna Gmail
MAIL_PASSWORD     = '<Storage@1/>'       # ← App Password
MAIL_FROM_NAME    = 'First Fullstack App'

# ── Reset Token Config ────────────────────────────────
RESET_TOKEN_EXPIRY_MINUTES = 15                 # 15 min mein expire
FRONTEND_URL               = 'http://localhost:4200'  # Angular URL