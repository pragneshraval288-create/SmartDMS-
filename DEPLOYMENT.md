# 🚀 Deploying SmartDMS (Production Guide)

SmartDMS ko production environment me safely deploy karne ke liye niche complete steps follow karein.

---

## ✅ 1. System Requirements

- Python 3.10+
- Virtualenv
- Gunicorn (WSGI Server)
- Nginx (Reverse Proxy)
- SQLite / PostgreSQL (recommended for production)
- Linux Server (Ubuntu 20.04+ recommended)

---

## ✅ 2. Clone & Install Dependencies

```bash
git clone https://github.com/yourusername/SmartDMS.git
cd SmartDMS
pip install -r requirements.txt
```

Agar production server Ubuntu ho:

```bash
sudo apt update
sudo apt install python3-venv python3-pip nginx -y
```

---

## ✅ 3. Environment Variables Set Karna

`.env.example` ko copy karke `.env` banaye:

```bash
cp .env.example .env
```

Inside `.env`, set:

```
SECRET_KEY=YOUR_SECURE_SECRET_KEY
FLASK_ENV=production
UPLOAD_FOLDER=backend/uploads
SESSION_COOKIE_SECURE=true
REMEMBER_COOKIE_SECURE=true
```

> PRO TIP: `SECRET_KEY` 32+ chars ka random string rakho.

---

## ✅ 4. Database Migration Setup (Flask-Migrate)

Production me **create_all() use mat karein**.

Initialize migration:

```bash
flask db init
flask db migrate
flask db upgrade
```

✅ Ye database versioning maintain rakhta hai.

---

## ✅ 5. Gunicorn Setup (Production WSGI Server)

Project root me run karein:

```bash
gunicorn --bind 0.0.0.0:8000 backend.app:create_app()
```

Test karein:

Open in browser:

```
http://your-server-ip:8000
```

---

## ✅ 6. Create a Gunicorn Service (Auto Start)

```
sudo nano /etc/systemd/system/smartdms.service
```

Paste:

```ini
[Unit]
Description=Gunicorn instance for SmartDMS
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/SmartDMS
Environment="PATH=/var/www/SmartDMS/venv/bin"
ExecStart=/var/www/SmartDMS/venv/bin/gunicorn --workers 3 --bind unix:smartdms.sock backend.app:create_app()

[Install]
WantedBy=multi-user.target
```

Phir:

```bash
sudo systemctl daemon-reload
sudo systemctl start smartdms
sudo systemctl enable smartdms
```

---

## ✅ 7. Nginx Reverse Proxy Setup

```
sudo nano /etc/nginx/sites-available/smartdms
```

Paste:

```nginx
server {
    listen 80;
    server_name your_domain_or_ip;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/SmartDMS/smartdms.sock;
    }

    location /static/ {
        alias /var/www/SmartDMS/static/;
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/smartdms /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

---

## ✅ 8. Enable HTTPS with Let’s Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com
```

Automatic HTTPS enabled ✅

---

## ✅ 9. Important Security Notes

✅ Never expose these folders:  
```
instance/
backend/database/
backend/uploads/
```

✅ Always set:
```
SESSION_COOKIE_SECURE=true
REMEMBER_COOKIE_SECURE=true
```

✅ Use:
```
FLASK_ENV=production
```

✅ Do NOT use debug mode on production.

✅ Use strong firewall rules.

---

## ✅ 10. Updating App (Zero Downtime)

```bash
git pull
flask db migrate
flask db upgrade
sudo systemctl restart smartdms
sudo systemctl restart nginx
```

---

## ✅ Deployment Summary (Short Version)

```
1. pip install -r requirements.txt
2. Setup .env
3. flask db migrate + upgrade
4. Run with Gunicorn
5. Serve via Nginx
6. Enable HTTPS
```

---

## ✅ Done! 🎉

SmartDMS successfully deployed on a secure production-grade server.


