import json
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

login_manager = LoginManager()

class User(UserMixin):
    def __init__(self, id_, username, password_hash):
        self.id = id_
        self.username = username
        self.password_hash = password_hash
    def verify(self, password):
        return check_password_hash(self.password_hash, password)

def load_users(path='users.json'):
    try:
        with open(path) as f:
            raw = json.load(f)
        users = {u['id']: User(u['id'], u['username'], u['password_hash']) for u in raw}
    except Exception:
        users = {}
    return users

USERS = load_users()

@login_manager.user_loader
def user_loader(user_id):
    return USERS.get(user_id)

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
