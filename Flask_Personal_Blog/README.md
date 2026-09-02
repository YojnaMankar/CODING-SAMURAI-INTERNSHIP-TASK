✨ Flask Personal Blog

A modern, secure and responsive personal blogging platform built with Python, Flask and SQLite.

This project was developed as part of the Coding Samurai Python Development Internship.

🌟 Highlights

Feature

Status

👤 User Registration & Login

✅

🔐 Password Hashing

✅

📊 Personal Dashboard

✅

✍️ Create Blog Posts

✅

✏️ Edit Posts

✅

🗑️ Delete Posts

✅

❤️ Like / Unlike Posts

✅

💬 Comments

✅

🔎 Search Posts

✅

🏷️ Category Filtering

✅

👤 User Profile

✅

📱 Responsive UI

✅

🔒 Environment-based Secret Key

✅

🖥️ Project Overview

Flask Personal Blog allows users to create and manage their own blog content through a clean web interface.

Users can:

Create an account and log in securely

Write and publish blog posts

Organize posts using categories

Edit or delete their own posts

Like and unlike posts

Read and add comments

Search posts by title, content, author or category

Filter posts by category

Manage content from a personal dashboard

View their profile and account information

🛠️ Tech Stack

Backend

🐍 Python 3

🌐 Flask

🔐 Werkzeug

🗄️ SQLite

⚙️ python-dotenv

Frontend

HTML5

CSS3

Jinja2 Templates

📂 Project Structure

Flask_Personal_Blog/
│
├── 📄 app.py
├── 📄 database.py
├── 📄 requirements.txt
├── 📄 README.md
├── 🔐 .env
├── 📄 .env.example
├── 📄 .gitignore
│
├── 📁 templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── create.html
│   ├── edit.html
│   ├── post_detail.html
│   └── profile.html
│
└── 📁 static/
    └── style.css

🚀 Getting Started

1️⃣ Clone the Repository

git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Flask_Personal_Blog

2️⃣ Create a Virtual Environment

Windows:

python -m venv venv
venv\Scripts\activate

3️⃣ Install Dependencies

pip install -r requirements.txt

🔐 Environment Configuration

Create a .env file in the project root:

SECRET_KEY=your-own-secret-key

The .env file contains private configuration and must not be uploaded to GitHub.

A safe template is provided in .env.example:

SECRET_KEY=your-secret-key-here

▶️ Run the Application

Start the Flask server:

python app.py

Open the application in your browser:

http://127.0.0.1:5000

🗄️ Database

The project uses SQLite through Python's built-in sqlite3 module.

The database handles:

👤 Users

📝 Blog Posts

❤️ Likes

💬 Comments

The local database file is excluded from GitHub using .gitignore.

🔒 Security

Security considerations implemented in this project include:

Passwords are hashed using Werkzeug

Flask session authentication protects private pages

Secret configuration is loaded from .env

.env is excluded from GitHub

Local database files are excluded from GitHub

Protected routes require user authentication

Never commit real API keys, passwords or secret keys to a public repository.

💡 What I Learned

Through this project, I practiced:

Building web applications with Flask

Routing and HTTP methods

Jinja2 template rendering

User authentication and sessions

Password hashing

CRUD operations

SQLite database integration

SQL queries and relationships

Form handling and validation

Search and filtering

Like and comment functionality

Responsive UI development

Managing secrets with environment variables

Preparing a project for GitHub

🔮 Future Improvements

Possible future enhancements:

🖼️ Blog image uploads

📝 Rich-text editor

📄 Pagination

🔔 Notifications

📧 Email verification

🔑 Password reset

👑 Admin panel

☁️ Cloud deployment

🌙 Dark mode

👩‍💻 Author

Yojna Mankar

Python Developer | Flask | SQLite | Web Development

🎓 Internship Project

Developed as part of the:

Coding Samurai — Python Development Internship

The internship project requirements include completing Python projects and uploading completed work to GitHub.

⭐ Project

If you find this project useful or interesting, consider giving the repository a ⭐ Star on GitHub!

📌 License

This project was created for educational and internship purposes.