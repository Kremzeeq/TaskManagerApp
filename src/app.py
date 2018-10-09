from flask import Flask, render_template
from src.common.database import Database

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = '123'

@app.before_first_request
def init_db():
    Database.initialize()

@app.route('/')
def home():
    return render_template('home.html')

from src.models.users.user_view import user_blueprint
from src.models.tasks.task_view import task_blueprint

app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(task_blueprint, url_prefix="/tasks")