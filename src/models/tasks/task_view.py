from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
from src.models.tasks.task_controller import Task
from src.models.users.user_controller import User
import src.models.users.user_decorators as user_decorators
import datetime

task_blueprint = Blueprint('tasks', __name__)

@task_blueprint.route('/task_portal', methods=['GET', 'POST'])
@user_decorators.requires_login
def task_portal():
    tasks = Task.find_task_docs_in_db()
    return render_template('tasks/task_portal.html', tasks=tasks)

@task_blueprint.route('/create_task', methods=['GET','POST'])
@user_decorators.requires_login
def create_task():
    if request.method == 'POST':
        task_name = request.form['task_name']
        priority = request.form['priority']
        description = request.form['description']
        task = Task(task_name, description, priority)
        email = session['email']
        task.user_id_task_owner = User.find_user_by_email(email)
        task.save_to_db()
        return redirect(url_for('tasks.task_portal'))
    return render_template('tasks/create_task.html')

@task_blueprint.route('/<string:task_id>')
@user_decorators.requires_login
def get_task_page(task_id):
    task = Task.find_by_id(task_id)
    return render_template('tasks/task.html', task=task)

@task_blueprint.route('/edit/<string:task_id>', methods=['GET','POST'])
@user_decorators.requires_login
def edit_task(task_id):
    task = Task.find_by_id(task_id)
    if request.method == 'POST':
        task.priority = request.form['priority']
        task.description = request.form['description']
        task.completed_by = request.form['completed_by']
        task.date_updated = datetime.datetime.utcnow()
        status_boolean = request.form.get('status_boolean')
        if len(task.completed_by) > 0 or status_boolean == "1":
            status_boolean = True
        elif task.completed_by == "" and status_boolean == None:
            status_boolean = False
        else:
            pass
        task.status = task.find_status_text(status_boolean)
        task.status_boolean = status_boolean
        task.save_to_db()
        return redirect(url_for('tasks.task_portal'))
    return render_template('tasks/edit_task.html', task=task)

@task_blueprint.route('/delete/<string:task_id>')
@user_decorators.requires_login
def delete_task(task_id):
    Task.find_by_id(task_id).delete()
    return redirect(url_for('tasks.task_portal'))