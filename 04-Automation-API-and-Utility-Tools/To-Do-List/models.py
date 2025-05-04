from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    due_date = db.Column(db.String(50))
    priority = db.Column(db.String(10))
    status = db.Column(db.String(20), default='todo')  # todo, inprogress, done
