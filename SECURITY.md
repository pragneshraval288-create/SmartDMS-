# 🔐 SmartDMS Security Hardening Guide

SmartDMS ek document management platform hai jisme user uploads, authentication aur role-based access included hai — isiliye system ko secure rakhna critical hai.  
Neeche complete hardening checklist di gayi hai.

---

## ✅ 1. Secret Key Management

- `SECRET_KEY` **never commit in code**  
- Always set via environment variable:

```
export SECRET_KEY="your-64-character-random-secret"
```

- Use long, random keys.  
- Rotate keys periodically.

---

## ✅ 2. Secure Upload Handling

### ✅ Uploads stored outside `/static`  
✅ Prevents direct public access  
✅ Forces access only through authenticated routes

### ✅ Allowed file types only  
Basic validation:

- `.pdf`
- `.docx`
- `.csv`
- `.txt`
- `.xlsx`

### ✅ Recommended: MIME validation with `python-magic`
```
filetype = magic.from_buffer(file.read(2048), mime=True)
```

### ✅ File size limit
Configured via `MAX_CONTENT_LENGTH`

Example:

```
MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20MB
```

### ✅ Clean stored filenames  
Avoid original names; generate safe UUID filenames.

---

## ✅ 3. Authentication Security

### ✅ Rate-limit login form
Applied via Flask-Limiter:

```
@limiter.limit("5 per minute")
```

Prevents brute-force attacks.

### ✅ Strong password hashing
Flask uses:

```
werkzeug.security.generate_password_hash()
```

(Which defaults to PBKDF2 → secure)

### ✅ Session Hardening

```
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE   = True
REMEMBER_COOKIE_SECURE  = True
```

---

## ✅ 4. Role-Based Access Control (RBAC)

### ✅ Admin
- Can view/edit/delete all documents  
- Can view all audit logs

### ✅ User
- Can only access own documents  
- Cannot view other user data  
- All routes protected via:

```
if not user_or_admin_owns(doc):
```

---

## ✅ 5. Audit Logging

Every action logged:

- upload  
- update  
- delete  
- download  

Stored in DB with:

- user_id  
- timestamp  
- filename  
- version  

✅ Helps detect misuse  
✅ Useful for admin monitoring  

---

## ✅ 6. Security Headers via `after_request`

SmartDMS sets:

- `X-Frame-Options: DENY`
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy: camera=(), microphone=(), geolocation=()`
- Strong CSP:

```
Content-Security-Policy:
default-src 'self' https://cdn.jsdelivr.net;
img-src 'self' data: https:;
style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net;
script-src 'self' https://cdn.jsdelivr.net
```

✅ Blocks XSS  
✅ Prevents clickjacking  
✅ Reduces attack surface

---

## ✅ 7. Flask Debug Mode

**Never turn on debug mode in production.**

- Disables auto browser-open  
- Removes Werkzeug debug console  
- Prevents RCE (remote code execution)

---

## ✅ 8. Production Database Recommendations

SQLite ✅ Good for local development  
PostgreSQL ✅ Recommended for deployment

Use Alembic migrations instead of `db.create_all()`:

```bash
flask db migrate
flask db upgrade
```

---

## ✅ 9. Avoid Direct Exposure of Sensitive Folders

Never expose:

- `/backend/uploads/`
- `/backend/database/`
- `/instance/`
- `.env`

Ensure Nginx blocks these paths.

---

## ✅ 10. HTTPS Only

Enable HTTPS via Let’s Encrypt:

```bash
sudo certbot --nginx -d yourdomain.com
```

Force HTTPS:

```
SESSION_COOKIE_SECURE = True
REMEMBER_COOKIE_SECURE = True
```

Protects against session hijacking.

---

## ✅ 11. Recommended Additional Hardening

✔ Add Captcha on login (optional)  
✔ Use fail2ban on login endpoint  
✔ Periodic cleanup of old document versions  
✔ Regular database backup  
✔ Long-term token invalidation  

---

## ✅ Summary Checklist

✅ Secret Key from environment  
✅ Safe uploads only  
✅ Rate-limited login  
✅ CSRF protection enabled  
✅ Strict security headers  
✅ Role-based permission checks  
✅ HTTPS mandatory  
✅ DB migrations in production  
✅ Sensitive directories hidden  
✅ Debug disabled

---

**SmartDMS is now hardened and production-ready.**  
If you need a security audit or code review — Himu is always here ❤️✨
