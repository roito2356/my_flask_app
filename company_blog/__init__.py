import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)

app.config["SECRET_KEY"] = "mysecretkey"
basedir = os.path.abspath(os.path.dirname(__file__))

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
uri = os.environ.get("DATABASE_URL")
if uri:
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
        app.config["SQLALCHEMY_DATABASE_URI"] = uri
else:
    # passwordにはインストール時に設定したパスワードを入力してください。
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:password@localhost"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)
Migrate(app, db)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"


def localize_callback(*args, **kwargs):
    return "このページにアクセスするには、ログインが必要です。"


login_manager.localize_callback = localize_callback


from company_blog.main.views import main
from company_blog.users.views import users
from company_blog.error_pages.handlers import error_pages

app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(error_pages)
