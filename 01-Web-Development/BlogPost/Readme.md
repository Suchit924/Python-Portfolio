# ✍️ Blog Post Platform

A blog web application with full CRUD functionality, allowing users to create, read, update, and delete blog posts.

## Live Demo

You can view the live website at:  
[Suchit Blogs](https://suchit-blogs-abkj.onrender.com)

## Features

- User authentication and login system.
- Post creation, viewing, and deletion.
- Comment system on blog posts.
- Gravatar integration for user avatars.
- Responsive design using Bootstrap.

## Technologies Used

- **Flask**: Web framework for Python.
- **SQLAlchemy**: ORM for interacting with databases.
- **Flask-SQLAlchemy**: Flask extension for SQLAlchemy integration.
- **Flask-Login**: User session management.
- **Flask-WTF**: Forms handling.
- **Bootstrap**: Frontend framework for responsive design.
- **Gunicorn**: WSGI server for running Flask in production.
- **PostgreSQL**: Database used for storing blog posts and user information.
- **Flask-CKEditor**: Rich text editor for creating blog posts.

## Setup Instructions

To run this project locally, follow the steps below.
1. Clone the repository
```bash
git clone https://github.com/Suchit924/Suchit_Blogs.git
cd Suchit_Blogs
```
2. Set up the virtual environment
```bash
python -m venv venv
source venv/bin/activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
FLASK_APP=main.py
FLASK_ENV=development
FLASK_KEY: Generate a secret key for Flask sessions.
DB_URI: Provide your PostgreSQL database URI.
```
5. Run the application
```bash
flask run
```
## Project Structure
```bash
Suchit_Blogs/
│
├── app/              # Main application files
│   ├── __init__.py
│   ├── routes.py     # All routes and views
│   └── models.py     # Database models
│
├── templates/        # HTML templates
├── static/           # Static files (CSS, JS, images)
├── requirements.txt  # Python dependencies
├── .env              # Environment variables
└── README.md         # Project documentation
