# 🎯 Goal Tracker

**Goal Tracker** is a simple, beautiful, and RTL-friendly goal tracking web application built with Flask.  
It allows users to define goals, log daily progress, and view visual reports with charts.

---

## 🚀 Features

- ✅ User authentication (Register/Login/Logout)
- 🎯 Add, edit, and delete goals
- 📝 Track daily progress for each goal
- 📊 View reports with beautiful charts and progress bars
- 🌙 Light and Dark themes ready (customizable)
- 🌐 RTL (Right-To-Left) support for Persian users
- 🔒 Password validation with strong rules
- 💬 Flash messages and form validation in Persian

---

## 🛠 Tech Stack

- **Backend:** Python, Flask, Flask-WTF
- **Frontend:** HTML, CSS (custom), Chart.js
- **Database:** SQLite (via SQLAlchemy)
- **Templating:** Jinja2

---

## 📂 Folder Structure

```
Goal-Tracker/
│
├── static/
│   ├── style.css
│   ├── fonts/
│   └── images/
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── report.html
│   ├── login.html
│   └── ...
│
├── app.py
├── models.py
├── forms.py
├── site.db
├── ColorCodes.txt
├── requirements.txt
└── README.md  ← You are here!
```

---

## ⚙️ Setup Instructions

1. **Clone the project**  
   `git clone https://github.com/Aparsash/goal-tracker.git`

2. **Navigate into the folder**  
   `cd goal-tracker`

3. **Create a virtual environment & activate it**  
   `python -m venv venv`  
   `source venv/bin/activate` (Linux/Mac)  
   `venv\Scripts\activate` (Windows)

4. **Install dependencies**  
   `pip install -r requirements.txt`

5. **Run the app**  
   `python app.py`

6. Open in browser: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📌 Deployment Tips

For free hosting, you can use platforms like:

- [Render](https://render.com/)
- [Fly.io](https://fly.io/)
- [Railway](https://railway.app/)

_(Note: They support backend deployment with SQLite and Flask)_

---

## 📧 Author

Made with ❤️ by **Parsa**  
For questions or feedback, feel free to connect ✌️

