import os
import logging
import threading
import webbrowser

from flask import Flask
from flask_login import current_user

# ✅ absolute imports
from backend.config import Config, TEMPLATE_DIR, STATIC_DIR
from backend.extensions import db, login_manager, migrate, csrf, limiter


def create_app():
    app = Flask(
        __name__,
        template_folder=TEMPLATE_DIR,
        static_folder=STATIC_DIR
    )

    # ✅ Load config
    app.config.from_object(Config)

    # ✅ Ensure upload folder exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # ✅ Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    limiter.init_app(app)

    login_manager.login_view = "auth.login"

    # ✅ global current_user
    @app.context_processor
    def inject_user():
        return dict(current_user=current_user)

    # ✅ Register blueprints
    from backend.routes import auth, dashboard, documents, history, api
    from backend.routes.profile import bp as profile_bp

    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(documents.bp)
    app.register_blueprint(history.bp)
    app.register_blueprint(api.bp)

    # ✅ VERY IMPORTANT: URL Prefix for Profile
    app.register_blueprint(profile_bp, url_prefix="/profile")

    # ✅ Security headers
    @app.after_request
    def after(resp):
        resp.headers.setdefault("X-Content-Type-Options", "nosniff")
        resp.headers.setdefault("X-Frame-Options", "DENY")
        resp.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        resp.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        return resp

    # ✅ Logging
    logging.basicConfig(
        filename="backend.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    return app


# ✅ AUTO RUNNER
def run_app():
    app = create_app()

    def open_browser():
        try:
            webbrowser.open_new("http://127.0.0.1:5000/")
        except:
            pass

    threading.Timer(1.0, open_browser).start()

    with app.app_context():
        db.create_all()

    app.run(debug=True)


if __name__ == "__main__":
    import sys
    ROOT = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(ROOT)

    if PROJECT_ROOT not in sys.path:
        sys.path.insert(0, PROJECT_ROOT)

    run_app()
