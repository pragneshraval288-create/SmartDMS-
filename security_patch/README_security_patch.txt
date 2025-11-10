SmartDMS Security Patch
=======================

This folder contains a set of security improvements and an automated patcher `apply_patch.py`
that will try to inject safer authentication and app-setup code into your existing project.

What it adds:
- Secure password hashing (werkzeug)
- Rate limits on auth endpoints (Flask-Limiter)
- CSRF protection (Flask-WTF already present)
- Guidance to enable Flask-Talisman (HTTPS headers)
- Upload validation helper
- A ready-to-register `auth` blueprint (security_patch/secure_auth.py)

How to use:
1. Backup your project.
2. Run `python security_patch/apply_patch.py` from the project root. It will:
   - attempt to replace placeholders '...' in backend/app.py and backend/routes/auth.py
     with safer implementations.
   - create `backend/security_helpers.py` with upload validation utilities.
3. Review changes, run tests, and then run the app.

If automated patching fails, manually:
- Copy `security_patch/secure_auth.py` into `backend/routes/secure_auth.py`
- Register the blueprint in your app factory:
    from backend.routes.secure_auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

Remember: Always test in a development environment first.
