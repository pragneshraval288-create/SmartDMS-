import os
import logging
import threading
import webbrowser
from datetime import timedelta

from flask import Flask
from flask_login import current_user

# ✅ absolute imports — NEVER relative when running backend/app.py directly
from backend.config import Config, TEMPLATE_DIR, STATIC_DIR
from backend.extensions import db, login_manager, migrate, csrf, limiter
from backend.models import User


def create_app():
    app = Flask(
        __name__,
        template_folder=TEMPLATE_DIR,
        static_folder=STATIC_DIR
    )

    # ✅ load config
    app.config.from_object(Config)

    # ✅ ensure upload folder exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # ✅ initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    limiter.init_app(app)

    login_manager.login_view = "auth.login"

    # ✅ inject current user globally (for username + role)
    @app.context_processor
    def inject_user():
        return dict(current_user=current_user)

    # ✅ register all blueprints using absolute imports
    from backend.routes import auth, dashboard, documents, history, api
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(documents.bp)
    app.register_blueprint(history.bp)
    app.register_blueprint(api.bp)

    # ✅ security headers
    @app.after_request
    def _headers(resp):
        resp.headers.setdefault("X-Content-Type-Options", "nosniff")
        resp.headers.setdefault("X-Frame-Options", "DENY")
        resp.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        resp.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        return resp

    # ✅ logging
    logging.basicConfig(
        filename="backend.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    return app


# ✅ AUTO-RUNNER
def run_app():

    app = create_app()

    # ✅ auto-open browser
    def open_browser():
        try:
            webbrowser.open_new("http://127.0.0.1:5000/")
        except:
            pass

    threading.Timer(1.0, open_browser).start()

    # ✅ auto-create database tables
    with app.app_context():
        db.create_all()

    # ✅ run server
    app.run(debug=True)


# ✅ DIRECT RUN SUPPORT (run button)
if __name__ == "__main__":
    # ✅ ensure project root added to Python path
    import sys
    ROOT = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(ROOT)

    if PROJECT_ROOT not in sys.path:
        sys.path.insert(0, PROJECT_ROOT)

    run_app()
