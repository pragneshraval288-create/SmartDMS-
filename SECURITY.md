🔐 SmartDMS Security Hardening Guide

SmartDMS is a document management platform that includes user file uploads, authentication, and role-based access.
Because of these features, keeping the system secure is critical.

This document provides a complete hardening checklist for making SmartDMS production-ready.

------------------------------------------------------------

✅ 1. Secret Key Management
- Never commit SECRET_KEY to the repository
- Always load via environment variables:
export SECRET_KEY="your-64-character-random-secret"
- Use long, cryptographically secure keys
- Rotate keys periodically

------------------------------------------------------------

✅ 2. Secure File Upload Handling
- Uploads stored outside /static to prevent direct access
- Allowed file types:
  .pdf, .docx, .csv, .txt, .xlsx
- Validate MIME type using python-magic
- Enforce file size limit:
  MAX_CONTENT_LENGTH = 20 * 1024 * 1024
- Use safe filenames (UUID-based)

------------------------------------------------------------

✅ 3. Authentication Security
- Rate-limited login (Flask-Limiter: 5 per minute)
- Strong password hashing (Werkzeug / Argon2)
- Secure session cookies:
  SESSION_COOKIE_HTTPONLY = True
  SESSION_COOKIE_SECURE   = True
  REMEMBER_COOKIE_SECURE  = True

------------------------------------------------------------

✅ 4. Role-Based Access Control (RBAC)
Admin:
- Full access to all documents
- View all logs

User:
- Access only their documents

------------------------------------------------------------

✅ 5. Audit Logging
Every action is logged:
- upload, update, delete, download
Logs include timestamp, user_id, filename, version

------------------------------------------------------------

✅ 6. Security Headers
Automatically set headers:
- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff
- Referrer-Policy: strict-origin-when-cross-origin
- Permissions-Policy: camera=(), microphone=(), geolocation=()
- CSP applied

------------------------------------------------------------

✅ 7. Flask Debug Mode
Never enable in production.

------------------------------------------------------------

✅ 8. Production Database
- SQLite for development
- PostgreSQL recommended for production
Use migrations:
flask db migrate
flask db upgrade

------------------------------------------------------------

✅ 9. Hide Sensitive Directories
Never expose:
- backend/uploads/
- backend/database/
- instance/
- .env
- Backups

------------------------------------------------------------

✅ 10. Enforce HTTPS
Enable HTTPS via Certbot:
sudo certbot --nginx -d yourdomain.com
Force secure cookies.

------------------------------------------------------------

✅ 11. Additional Recommended Hardening
- Add captcha to login page
- Enable fail2ban
- Delete old file versions
- Automated database backups
- Short session expiry
- Strong password policies

------------------------------------------------------------

✅ Final Security Checklist
✅ Secret key via environment
✅ Secure upload folder
✅ Login rate-limited
✅ CSRF enabled
✅ Security headers enabled
✅ RBAC active
✅ HTTPS enabled
✅ PostgreSQL recommended
✅ Sensitive directories hidden
✅ Debug disabled

