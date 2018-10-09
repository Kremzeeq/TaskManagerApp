from flask import Blueprint, request, session, url_for, render_template
import src.models.users.user_errors as UserErrors

from src.models.users.user_controller import User

from werkzeug.utils import redirect

user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/sign_up', methods=['GET', 'POST'])
def sign_up_email():
    if request.method == 'POST':
        email=request.form['email']
        try:
            user_data= User(email)
            user_data.check_email_valid()
            user_data.send_auth_code_email()
            return redirect("/")
        except UserErrors.UserError as e:
            return e.message
    return render_template("users/sign_up.html")

@user_blueprint.route('/auth', methods=['GET','POST'])
def authenticate_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            if User.authenticate_user(email, password):
                return redirect(url_for("users.register_user"))
        except UserErrors.UserError as e:
            return e.message
    return render_template("users/auth.html")

@user_blueprint.route('/register', methods=['GET','POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            if User.register_user(email, password):
                session['email'] = email
                session['user_id'] = User.find_user_by_email(email)
                return redirect(url_for("tasks.task_portal"))
        except UserErrors.UserError as e:
            return e.message
    return render_template("users/register.html")

@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            if User.validate_user_login(email, password):
                session['email'] = email
                session['user_id'] = User.find_user_by_email(email)
                return redirect(url_for("tasks.task_portal"))
        except UserErrors.UserError as e:
            return e.message
    return render_template("users/login.html")

@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    session['user_id'] = None
    return redirect("/")


