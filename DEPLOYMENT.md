🚀 SmartDMS – Production Deployment Guide

This guide explains how to deploy SmartDMS on a production server using Gunicorn + Nginx, with proper security, environment variables, and performance optimizations.

------------------------------------------------------------

✅ 1. System Requirements
- Python 3.10+
- Linux Server (Ubuntu 20.04 / 22.04 recommended)
- Gunicorn (WSGI production server)
- Nginx (Reverse Proxy)
- SQLite (default) / PostgreSQL (optional)
- Virtual Environment (venv)

------------------------------------------------------------

✅ 2. Clone the Project & Install Dependencies

Clone repository:
git clone https://github.com/pragneshraval288-create/SmartDMS-.git
cd SmartDMS

Create & activate virtual environment:
python3 -m venv venv
source venv/bin/activate

Install project dependencies:
pip install -r requirements.txt

Install required server packages (Ubuntu):
sudo apt update
sudo apt install python3-venv python3-pip nginx -y

------------------------------------------------------------

✅ 3. Configure Environment Variables (.env)

Create .env file:
SECRET_KEY=YOUR_SECURE_SECRET_KEY
FLASK_ENV=production
UPLOAD_FOLDER=backend/uploads
SESSION_COOKIE_SECURE=true
REMEMBER_COOKIE_SECURE=true

------------------------------------------------------------

✅ 4. Database Setup (Optional)

SmartDMS uses SQLite by default.
If using PostgreSQL:
DATABASE_URL=postgresql://username:password@localhost:5432/smartdms

------------------------------------------------------------

✅ 5. Run SmartDMS Using Gunicorn
gunicorn --bind 0.0.0.0:8000 backend.app:app

Visit:
http://YOUR-SERVER-IP:8000

------------------------------------------------------------

✅ 6. Create Gunicorn Service (Auto Start on Boot)

sudo nano /etc/systemd/system/smartdms.service

[Unit]
Description=Gunicorn SmartDMS Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/SmartDMS
Environment="PATH=/var/www/SmartDMS/venv/bin"
ExecStart=/var/www/SmartDMS/venv/bin/gunicorn --workers 3 --bind unix:/var/www/SmartDMS/smartdms.sock backend.app:app

[Install]
WantedBy=multi-user.target

Enable service:
sudo systemctl daemon-reload
sudo systemctl start smartdms
sudo systemctl enable smartdms

------------------------------------------------------------

✅ 7. Configure Nginx Reverse Proxy

sudo nano /etc/nginx/sites-available/smartdms

server {
    listen 80;
    server_name YOUR_DOMAIN_OR_IP;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/SmartDMS/smartdms.sock;
    }

    location /static/ {
        alias /var/www/SmartDMS/Frontend/static/;
    }
}

Enable configuration:
sudo ln -s /etc/nginx/sites-available/smartdms /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx

------------------------------------------------------------

✅ 8. Enable HTTPS (SSL Certificate)

Install Certbot:
sudo apt install certbot python3-certbot-nginx -y

Enable HTTPS:
sudo certbot --nginx -d yourdomain.com

✅ SSL enabled  
✅ Auto renewal configured

------------------------------------------------------------

✅ 9. Important Security Rules

Never expose:
backend/uploads/
backend/database/
instance/

Always set:
SESSION_COOKIE_SECURE=true
REMEMBER_COOKIE_SECURE=true
FLASK_ENV=production

Never run:
debug=True

Enable firewall:
sudo ufw enable
sudo ufw allow 'Nginx Full'

------------------------------------------------------------

✅ 10. Updating SmartDMS (Zero Downtime)

git pull
sudo systemctl restart smartdms
sudo systemctl restart nginx

------------------------------------------------------------

✅ Quick Deployment Summary
1. Clone project
2. Create & activate venv
3. Install requirements
4. Create .env file
5. Start Gunicorn
6. Configure Nginx
7. Add SSL
8. Restart all services

------------------------------------------------------------

✅ Deployment Complete 🎉
SmartDMS is now fully deployed and production-ready.

