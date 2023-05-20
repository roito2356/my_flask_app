from datetime import datetime
from pytz import timezone #s10-94
from werkzeug.security import check_password_hash, generate_password_hash #'check_password_hash's11-120, 'generate_password_hash's11-125
from flask_login import UserMixin # 'UserMixin's11-120

from company_blog import db, login_manager

# s11-119 ログインマネージャーの設定 start
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
# s11-119 ログインマネージャーの設定 end

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    administrator = db.Column(db.String(1))
    post = db.relationship('BlogPost', backref='author', lazy='dynamic') #s10-95

    def __init__(self, email, username, password, administrator):
        self.email = email
        self.username = username
        self.password = password # s11-125でpassword_hashからpasswordに変更
        self.administrator = administrator

    def __repr__(self):
        return f"UserName: {self.username}"

    # s11-120 Userモデルの変更 start
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    # s11-120 Userモデルの変更 end

    # s11-125 ユーザー登録時のパスワードのハッシュ化 start
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    # s11-125 ユーザー登録時のパスワードのハッシュ化 end

    # s11-129 権限制御１：モデルの編集 start
    def is_administrator(self):
        if self.administrator == "1":
            return 1
        else:
            return 0
    # s11-129 権限制御１：モデルの編集 end
    
    # s15-209 ユーザー管理ページ(ブログ投稿数)２：モデルの編集 start
    def count_posts(self, userid):
        return BlogPost.query.filter_by(user_id=userid).count()
    # s15-209 ユーザー管理ページ(ブログ投稿数)２：モデルの編集 end

# s9-94 ブログ投稿の管理モデルを定義 start URL:https://www.udemy.com/course/python-flask-webdevelopment/learn/lecture/33987288#questions
class BlogPost(db.Model):
    __tablename__ = 'blog_post'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('blog_category.id')) # s13-150
    date = db.Column(db.DateTime, default=datetime.now(timezone('Asia/Tokyo')))
    title = db.Column(db.String(140))
    text = db.Column(db.Text)
    summary = db.Column(db.String(140))
    featured_image = db.Column(db.String(140))

    def __init__(self, title, text, featured_image, user_id, category_id, summary): # 'category_id's13-150
        self.title = title
        self.text = text
        self.featured_image = featured_image
        self.user_id = user_id
        self.category_id = category_id # 'category_id's13-150
        self.summary = summary

    def __repr__(self):
        return f"PostID: {self.id}, Title: {self.title}, Author: {self.author} \n" #左の第三引数はs10-95で追加
# s9-94 ブログ投稿の管理モデルを定義 end

# s13-150 モデルの作成 start
# ブログカテゴリーモデル
class BlogCategory(db.Model):
    __tablename__ = 'blog_category'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(140))
    posts = db.relationship('BlogPost', backref='blogcategory', lazy='dynamic')
    
    def __init__(self, category):
        self.category = category

    def __repr__(self):
        return f"CategoryID: {self.id}, CategoryName: {self.category} \n"
    
    # s15-206 カテゴリ管理ページ(ブログ投稿数)２：view関数の追加 start
    # def count_posts(self, id):
    #     return BlogPost.query.filter_by(category_id=id).count()
    # s15-206 カテゴリ管理ページ(ブログ投稿数)２：view関数の追加 end

# お問合せフォームモデル
class Inquiry(db.Model):
    __tablename__ = 'inquiry'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    title = db.Column(db.String(140))
    text = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.now(timezone('Asia/Tokyo')))

    def __init__(self, name, email, title, text):
        self.name = name
        self.email = email
        self.title = title
        self.text = text

    def __repr__(self):
        return f"InquiryID: {self.id}, Name: {self.name}, Text: {self.text} \n"
# s13-150 モデルの作成 end