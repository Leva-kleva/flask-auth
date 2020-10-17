import json

from flask import Flask, redirect, url_for, request, make_response, render_template
from flask_login import login_user, LoginManager, UserMixin, current_user, login_required, logout_user

import data
import schemes


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


def template_response(body, code, is_json=False):
    if not is_json:
        status = "info" if code < 400 else "error"
        tmp = f'{{"{status}": "{body}"}}'
        body = tmp
    response = make_response(body, code)
    response.headers["Content-Type"] = "application/json"
    return response


class User(UserMixin):
    def __init__(self, user):
        self.user = user

    def get_id(self):
        object_id = self.user["id"]
        return str(object_id)


@login_manager.user_loader
def load_user(user_id):
    ans = data.execute(data.query.get_user_by_id, {"user_id": user_id}, array=False, to_json=False)
    return User(ans)


@app.errorhandler(404)
def not_found(error):
    return template_response("Not found", 404)


@app.route('/')
def index():
    return template_response("OK", 200)


@app.route('/signup', methods=['GET'])
def signup():
    #return render_template("signup.html")
    return template_response("OK", 200)


@app.route('/signup', methods=['POST'])
def signup_post():
    if not schemes.check(request, schemes.signup.post):
        return template_response('Невалидный запрос', 400)

    email = request.json['email']
    name = request.json['username']
    password = request.json['password']

    ans = data.execute(data.query.create_user, {"name": name, "password": password, "email": email})

    #body, code = data.errors(ans, body="OK", code="201")

    if ans == data.Errors.unprocessable_entity:
        return template_response('Email or login уже существует', 422)

    if ans == data.Errors.invalid_request:
        return template_response('invalid_request', 400)

    if ans == data.Errors.database_not_avalable:
        return template_response('Server Error', 500)

    return template_response("OK", 201)


@app.route('/login', methods=['GET'])
def login():
    #return render_template("login.html")
    return template_response('OK', 200)


@app.route('/login', methods=['POST'])
def login_post():
    if not schemes.check(request, schemes.login.post):
        return template_response('Невалидный запрос', 400)

    email = request.json['email']
    password = request.json['password']

    ans = data.execute(data.query.get_user, {"password": password, "email": email}, array=False, to_json=False)

    if ans is None:
        return template_response('ошибка в логине или пароле', 400)

    if ans == data.Errors.invalid_request:
        return template_response('invalid_request', 400)

    if ans == data.Errors.database_not_avalable:
        return template_response('Server Error', 500)

    loginuser = User(ans)
    login_user(loginuser)
    return template_response('OK', 202)


@app.route('/login', methods=['DELETE'])
@login_required
def login_delete():
    ans = data.execute(data.query.delete_user, {"email": current_user.user['email']})

    if ans == data.Errors.invalid_request:
        return template_response('invalid_request', 400)

    if ans == data.Errors.database_not_avalable:
        return template_response('Server Error', 500)

    return template_response('OK', 200)


@app.route('/login', methods=['PUT'])
@login_required
def login_put():
    if not schemes.check(request, schemes.login.put):
        return template_response('Невалидный запрос', 400)

    password = request.json['password']

    ans = data.execute(data.query.change_user_password, {"password": password, "email": current_user.user['email']})

    if ans == data.Errors.invalid_request:
        return template_response('invalid_request', 400)

    if ans == data.Errors.database_not_avalable:
        return template_response('Server Error', 500)

    return template_response('OK', 200)


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
    #return render_template("profile.html", user=result)
    return template_response(ans, 200, is_json=True)


if __name__ == '__main__':
    app.run(debug=True)
