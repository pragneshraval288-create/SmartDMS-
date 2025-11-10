# 📁 SmartDMS – Document Management System (Flask)

SmartDMS is a secure, lightweight, and user-friendly **Document Management System** built using **Flask + SQLite**.  
It provides authentication, role-based access, secure password validation, and a clean Bootstrap UI for document handling.

---

# ✅ Features

## 🔐 Authentication & Security
- Secure Login & Logout
- Password Hashing (Werkzeug)
- Strict Password Policy  
  ✅ Uppercase + lowercase + 1 special (@ # $ % ^ & *) + digits  
- Password Reset  
- SQL Injection Safe (SQLAlchemy ORM)
- Show/Hide Password Toggle
- Flash Alerts (Success / Error)

---

## 📁 Document Management
- Upload Documents
- View & Download Files
- Delete Documents
- Search by Document Title
- Only allowed file types:
  - pdf  
  - docx  
  - txt  
  - png  
  - jpg  

---

## 👥 Role-Based Access
- **Admin** → Full Access  
- **User** → Limited Access  

Choose role at registration.

---

## 🎨 Frontend UI (Bootstrap 5)
- Clean & Modern Layout
- Sidebar Navigation
- Dashboard Components
- Flash Message Support
- Responsive Design

---

# 🛠 Tech Stack

| Component | Technology |
|----------|------------|
| Backend  | Flask (Python) |
| Database | SQLite |
| Auth     | Flask-Login |
| Forms    | Flask-WTF |
| UI       | Bootstrap 5 |
| Security | Werkzeug, Custom Password Validator |

---

# 📂 Folder Structure

SmartDMS/
│
├── backend/
│ ├── app.py
│ ├── config.py
│ ├── extensions.py
│ ├── security_helpers.py
│ ├── models/
│ ├── routes/
│ └── uploads/ (created automatically if not present)
│
├── Frontend/
│ ├── templates/
│ └── static/
│
├── requirements.txt
├── README.md
└── DEPLOYMENT.md

yaml
Copy code

---

# 🚀 Installation & Setup

## 1️⃣ Clone the Project

```bash
git clone https://github.com/pragneshraval288-create/SmartDMS-
cd SmartDMS
2️⃣ Create Virtual Environment
Windows:

bash
Copy code
python -m venv venv
venv\Scripts\activate
Linux/macOS:

bash
Copy code
python3 -m venv venv
source venv/bin/activate
3️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Run the Application
bash
Copy code
python backend/app.py
✅ Opens in browser automatically
✅ Works from VS Code Run button

🔑 Password Policy (Custom Rule)
SmartDMS enforces this strict password format:

✅ Must contain:

1 Uppercase letter

1 or more lowercase letters

Exactly 1 special character: @ # $ % ^ & *

Ends with digits

✅ Examples (Valid):

perl
Copy code
Pragnesh@8849
Aaaa#123
Himu$987
❌ Examples (Invalid):

perl
Copy code
pragnesh@8849       (uppercase missing)
Pragnesh@@8849      (more than 1 special)
Pragnesh8849        (no special)
12345               (invalid format)
📦 Environment Variables (Optional)
Create .env file:

ini
Copy code
SECRET_KEY=your_secret_key
UPLOAD_FOLDER=backend/uploads
MAX_CONTENT_LENGTH=16MB
📝 Deployment
Production deployment guide is available in:

✅ DEPLOYMENT.md

Includes:

Gunicorn setup

Nginx reverse proxy

HTTPS setup

Environment variables

SQLite / PostgreSQL config

🎯 Future Improvements
Document Version Control

Audit Logs

Detailed Activity Tracking

Tags & Advanced Search

Pagination for Large File Lists

JWT Authentication (for mobile app support)

Docker Deployment

✅ License
MIT License © 2025 — Pragnesh Raval

✨ Author
Pragnesh Raval