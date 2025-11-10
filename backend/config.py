import os
import pathlib
import secrets

# ✅ Base directories
BASE_DIR = pathlib.Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"

# ✅ Template & Static directories (correct)
TEMPLATE_DIR = FRONTEND_DIR / "templates"
STATIC_DIR = FRONTEND_DIR / "static"

# ✅ Instance directory
INSTANCE_DIR = PROJECT_ROOT / "instance"


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(32)

    # ✅ Correct SQLite DB path
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or f"sqlite:///{BASE_DIR / 'database' / 'app.db'}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAX_CONTENT_LENGTH = int(os.environ.get("MAX_CONTENT_LENGTH_MB", "10")) * 1024 * 1024

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "false").lower() == "true"

    # ✅ Upload folder
    UPLOAD_FOLDER = str(INSTANCE_DIR / "uploads")

    REMEMBER_COOKIE_DURATION_DAYS = int(os.environ.get("REMEMBER_COOKIE_DAYS", "1"))
