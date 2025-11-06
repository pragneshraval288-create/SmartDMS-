# 📁 SmartDMS – Document Management System (Flask)

SmartDMS is a lightweight, fast, secure, and user-friendly **Document Management System** built using Flask.  
It includes separate permissions for Admin and Regular Users.

---

## ✅ Features

### 🔐 Authentication
- Secure Login / Logout  
- Role-based Access (Admin / User)  
- Password Reset  

### 📁 Document Management
- Upload documents  
- Edit document details  
- Full document versioning (v1, v2, v3...)  
- Delete documents  
- View / Preview / Download  
- Search by title, tags, and file type  
- Users can access only their own documents (Admin has full access)

### 📝 Activity Audit Log
- Tracks which user performed which action  
- Actions include upload / download / update / delete  
- Timestamp + version tracking  

### 📊 Dashboard
- Total documents  
- This week’s uploads  
- Recent activity  

### ✅ Admin Capabilities
- Can view/manage all documents  
- Can read all audit logs  
- Normal users are restricted only to their own data  

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Flask**
- **Flask-Login**
- **Flask-WTF**
- **Flask-Migrate**
- **SQLite Database**
- **Bootstrap 5**

---

## 📂 Folder Structure

SmartDMS/
│
├── backend/
│ ├── app.py
│ ├── config.py
│ ├── extensions.py
│ ├── models/
│ ├── routes/
│ ├── utils/
│ └── database/
│
├── templates/
├── static/
│ └── css/style.css
│
├── README.md
└── DEPLOYMENT.md

yaml
Copy code

---

## 🚀 Installation

### 1️⃣ Clone or Download the Project

```bash
git clone https://github.com/pragneshraval288-create/SmartDMS-
2️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
3️⃣ Run the Application
You can directly run:

bash
Copy code
python backend/app.py
✅ Automatically opens in your browser
✅ Works directly with VS Code’s Run button

🔑 Default Roles
You can choose a role during registration:

admin

user

Admin → Full system access
User → Can access only their own documents

📌 Environment Variables (Optional)
Create a .env file:

ini
Copy code
SECRET_KEY=your_secret_key
UPLOAD_FOLDER=backend/uploads
✅ Contributing
Pull Requests are welcome!
Feel free to add improvements, fixes, or new features.

✅ License
MIT License

✨ Author
Pragnesh Raval (SmartDMS Owner)
Developed with support from Parth Gadhavi and Yash Raval

yaml
Copy code

---

If you want, I can also generate:

✅ `DEPLOYMENT.md` (clean, professional)  
✅ GitHub project badges  
✅ A banner/logo for SmartDMS  
✅ API documentation  
