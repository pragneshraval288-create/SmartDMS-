import os, secrets, pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR.parent / 'templates'
STATIC_DIR   = BASE_DIR.parent / 'static'
INSTANCE_DIR = BASE_DIR.parent.parent / 'instance'

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f"sqlite:///{BASE_DIR / 'database' / 'app.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH_MB', '10')) * 1024 * 1024
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE','false').lower()=='true'
    UPLOAD_FOLDER = str(INSTANCE_DIR / 'uploads')
    REMEMBER_COOKIE_DURATION_DAYS = int(os.environ.get('REMEMBER_COOKIE_DAYS','1'))
