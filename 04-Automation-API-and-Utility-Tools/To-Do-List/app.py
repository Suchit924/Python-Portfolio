from flask import Flask, render_template, request, redirect, url_for
from models import db, Task

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    content = request.form.get('content')
    due_date = request.form.get('due_date')
    priority = request.form.get('priority')
    new_task = Task(content=content, due_date=due_date, priority=priority, status='todo')
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/move/<int:task_id>/<new_status>')
def move(task_id, new_status):
    task = Task.query.get(task_id)
    task.status = new_status
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
