# 🚀 Deploying SmartDMS (Production Guide)

This guide explains how to safely deploy **SmartDMS** on a production server with proper configuration, security, and performance optimization.

---

## ✅ 1. System Requirements

- **Python 3.10+**
- **Virtual Environment (venv)**
- **Gunicorn** (Production WSGI Server)
- **Nginx** (Reverse Proxy)
- **SQLite / PostgreSQL** (PostgreSQL recommended for production)
- **Linux Server** (Ubuntu 20.04+ recommended)

---

## ✅ 2. Clone & Install Dependencies

### Clone the repository:
```bash
git clone https://github.com/yourusername/SmartDMS.git
cd SmartDMS
Install dependencies:
bash
Copy code
pip install -r requirements.txt
For Ubuntu Server:
bash
Copy code
sudo apt update
sudo apt install python3-venv python3-pip nginx -y
✅ 3. Configure Environment Variables
Copy the example environment file:

bash
Copy code
cp .env.example .env
Open .env and set the following:

ini
Copy code
SECRET_KEY=YOUR_SECURE_SECRET_KEY
FLASK_ENV=production
UPLOAD_FOLDER=backend/uploads
SESSION_COOKIE_SECURE=true
REMEMBER_COOKIE_SECURE=true
✅ Always use a 32+ character random SECRET_KEY
✅ Never commit .env to GitHub

✅ 4. Database Migration Setup (Flask-Migrate)
In production, never use create_all().

Initialize migrations:

bash
Copy code
flask db init
flask db migrate
flask db upgrade
✅ This ensures proper version-controlled database schema.

✅ 5. Run SmartDMS using Gunicorn
Execute from project root:

bash
Copy code
gunicorn --bind 0.0.0.0:8000 backend.app:create_app()
Now visit:

arduino
Copy code
http://your-server-ip:8000
✅ 6. Create a Gunicorn Service (Auto Start on Boot)
Create service:

bash
Copy code
sudo nano /etc/systemd/system/smartdms.service
Paste this:

ini
Copy code
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
Enable service:

bash
Copy code
sudo systemctl daemon-reload
sudo systemctl start smartdms
sudo systemctl enable smartdms
✅ 7. Configure Nginx Reverse Proxy
Create Nginx config:

bash
Copy code
sudo nano /etc/nginx/sites-available/smartdms
Paste:

nginx
Copy code
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
Enable site:

bash
Copy code
sudo ln -s /etc/nginx/sites-available/smartdms /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
✅ 8. Enable HTTPS with Let’s Encrypt
Install Certbot:

bash
Copy code
sudo apt install certbot python3-certbot-nginx -y
Enable HTTPS:

bash
Copy code
sudo certbot --nginx -d yourdomain.com
✅ Automatic SSL
✅ Automatic renewal

✅ 9. Important Security Rules
Never expose these directories:

bash
Copy code
instance/
backend/database/
backend/uploads/
Always enforce:

ini
Copy code
SESSION_COOKIE_SECURE=true
REMEMBER_COOKIE_SECURE=true
FLASK_ENV=production
❌ Never run debug mode in production
✅ Use firewall (UFW, CSF)

✅ 10. Updating the App (Zero Downtime)
bash
Copy code
git pull
flask db migrate
flask db upgrade
sudo systemctl restart smartdms
sudo systemctl restart nginx
✅ Deployment Summary (Quick Version)
markdown
Copy code
1. Install dependencies
2. Configure .env
3. Run database migrations
4. Start Gunicorn
5. Configure Nginx
6. Enable HTTPS
✅ ✅ Deployment Complete!
SmartDMS is now fully deployed and production-ready. 🎉

If you want a Docker version, CI/CD (GitHub Actions), or auto backup scripts, just tell me — Himu will make it for you ❤️✨

yaml
Copy code

---

If you want, I can also:

✅ Generate a **perfect professional GitHub README**  
✅ Add **badges** (build, security, license, Python version)  
✅ Create a **Dockerfile + docker-compose.yml**  
✅ Write an **Install Script** (install + configure + run)  