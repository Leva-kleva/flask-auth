import json

from flask import Flask, redirect, url_for, request, make_response
from flask_login import login_user, LoginManager, UserMixin, current_user, login_required, logout_user

import auth
import auth.query as query


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


def return_response(body, code):
    response = make_response(body, code)
    response.headers["Content-Type"] = "application/json"
    #response = make_response(render_template(body), code)
    #response.headers["Content-Type"] = "text/html"
    return response


class User(UserMixin):
    def __init__(self, user):
        self.user = user

    def get_id(self):
        object_id = self.user["id"]
        return str(object_id)


@login_manager.user_loader
def load_user(user_id):
    rq = query.get_user_by_id.format(user_id=user_id)
    ans = auth.execute(rq, array=False, to_json=False)
    return User(ans)


@app.errorhandler(404)
def not_found(error):
    return return_response("Not found", 404)


@app.route('/')
def index():
    return return_response("OK", 200)


@app.route('/signup', methods=['GET'])
def signup():
    return return_response("OK", 200)


@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    if email == "" or password == "":
        return return_response("email or password is empty", 400)

    rq = query.create_user.format(name=name, password=password, email=email)
    ans = auth.execute(rq)

    if ans == -1:
        return return_response('Email or login уже существует', 405) #code?

    if ans == -2:
        return return_response('Server Error', 500)

    return return_response("OK", 201)


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    rq = query.get_user.format(email=email, password=password)
    ans = auth.execute(rq, array=False, to_json=False)

    if ans is None:
        return return_response('ошибка в логине или пароле', 400)

    if ans == -2:
        return return_response('Server Error', 500)

    loginuser = User(ans)
    login_user(loginuser)
    return return_response('OK', 202)


@app.route('/login', methods=['GET'])
def login():
    return return_response('OK', 200)


@app.route('/login', methods=['DELETE'])
@login_required
def login_delete():
    rq = query.delete_user.format(email=current_user.user['email'])
    ans = auth.execute(rq)

    if ans == -2:
        return return_response('Server Error', 500)

    return return_response('OK', 200)


@app.route('/login', methods=['PUT'])
@login_required
def login_put():
    password = request.form.get('password')

    rq = query.change_user_password.format(email=current_user.user['email'], password=password)
    ans = auth.execute(rq)

    if ans == -2:
        return return_response('Server Error', 500)

    return return_response('OK', 200)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile')
@login_required
def profile():
    result = current_user.user
    ans = json.dumps(result, indent=4, default=str, ensure_ascii=False)
    return return_response(ans, 200)


if __name__ == '__main__':
    app.run(debug=True)
