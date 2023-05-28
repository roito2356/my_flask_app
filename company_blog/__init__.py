import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager # 'LoginManager's11-119

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
# s17-265 完成版Webアプリの変更：データベース(PostgreSQL) start
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite') # s17-265でこのコードをコメントアウト
uri = os.environ.get('DATABASE_URL')
if uri:
    if uri.startswith('postgres://'):
        uri = uri.replace('postgres://', 'postgresql://', 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = uri
else:
    # passwordにはインストール時に設定したパスワードを入力してください。
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:aito0411@localhost'
# s17-265 完成版Webアプリの変更：データベース(PostgreSQL) end

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
Migrate(app, db)


# s11-119 ログインマネージャーの設定 start
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login' # 'users.'s12-143
# s11-119 ログインマネージャーの設定 end

# s11-128 未ログインユーザーからの保護 start
def localize_callback(*args, **kwargs):
    return 'このページにアクセスするには、ログインが必要です。'
login_manager.localize_callback = localize_callback
# s11-128 未ログインユーザーからの保護 end

# s17-265でこのコードをコメントアウト start
##s12-142でこの__init__.pyに移動
# s10-95 リレーションシップ設定3 start
# from sqlalchemy.engine import Engine
# from sqlalchemy import event

# @event.listens_for(Engine, "connect")
# def set_sqlite_pragma(dbapi_connection, connection_record):
#     cursor = dbapi_connection.cursor()
#     cursor.execute("PRAGMA foreign_keys=ON")
#     cursor.close()
# s10-95 リレーションシップ設定3 end
# s17-265でこのコードをコメントアウト end

from company_blog.main.views import main # s13-148 Blueprintの基本設定
# s12-143 各ファイルのコードの移行６：Blueprintの登録 start
from company_blog.users.views import users
from company_blog.error_pages.handlers import error_pages

app.register_blueprint(main)  # s13-148 Blueprintの基本設定
app.register_blueprint(users)
app.register_blueprint(error_pages)
# s12-143 各ファイルのコードの移行６：Blueprintの登録 end