# 📁 SmartDMS – Document Management System (Flask)

SmartDMS ek lightweight, fast, secure aur user-friendly **Document Management System** hai jo Flask par built hai.  
Isme admin aur normal user ke liye alag-alag permissions diye gaye hain.

---

## ✅ Features

### 🔐 Authentication
- Secure Login / Logout  
- Role-based Access (Admin / User)  
- Password Reset  

### 📁 Document Management
- Upload documents  
- Edit document details  
- Versioning system (v1, v2, v3...)  
- Delete documents  
- View / Preview / Download  
- Search by title, tags, and file type  
- User-only access to their own documents (Admin can access all)

### 📝 Activity Audit Log
- Kis user ne kya action kiya (upload/download/delete/update)  
- Timestamp + version tracking  

### 📊 Dashboard
- Total documents  
- This week uploads  
- Recent activity  

### ✅ Admin Capabilities
- Can view/manage all documents  
- Can see all audit logs  
- Users restricted only to their own docs  

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

```
SmartDMS/
│
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── extensions.py
│   ├── models/
│   ├── routes/
│   ├── utils/
│   └── database/
│
├── templates/
├── static/
│   └── css/style.css
│
├── README.md
└── DEPLOYMENT.md
```

---

## 🚀 Installation

### 1️⃣ Clone or Download Project
```bash
git clone https://github.com/pragneshraval288-create/SmartDMS-
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the App
Aap direct `backend/app.py` run kar sakte ho:

✅ Browser automatically open ho jayega

```bash
python backend/app.py
```

or  

✅ Run button (VS Code)

---

## 🔑 Default Roles

User registration ke time tum role choose kar sakte ho:

- **admin**
- **user**

Admin = full access  
User = only own documents access  

---

## 📌 Environment Variables (Optional)

`.env` file me yeh rakhen:

```
SECRET_KEY=your_secret_key
UPLOAD_FOLDER=backend/uploads
```

---

## ✅ Contributing
PRs welcome!  

---

## ✅ License
MIT License

---

## ✨ Author
**Pragnesh Raval (SmartDMS Owner)**  
**Parth Gadhavi (SmartDMS Owner)** 
**Yash Raval (SmartDMS Owner)** 

