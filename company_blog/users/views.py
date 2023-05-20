from flask import render_template, url_for, redirect, session, flash, request, abort # 'abort's11-129
from flask_login import login_user, logout_user, login_required, current_user # 'login_user's11-122, 'logout_user's11-127, 'login_required's11-128, 'current_user's11-129
# s12-141 各ファイルのコードの移行４：views.py start
from company_blog import db
from company_blog.models import User, BlogPost, BlogCategory # 'BlogPost, BlogCategory's15-210
from company_blog.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from company_blog.main.forms import BlogSearchForm # s15-210
from flask import Blueprint

users = Blueprint('users', __name__)
# s12-141 各ファイルのコードの移行４：views.py end

# s11-122 ログイン用view関数の追加 start
@users.route('/login', methods=['GET', 'POST']) # 'users's12-141
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            if user.check_password(form.password.data):
                login_user(user)
                next = request.args.get('next')
                if next == None or not next[0] == '/':
                    next = url_for('users.user_maintenance') # 'users.'s12-141
                return redirect(next)
            else:
                flash('パスワードが一致しません')
        else:
            flash('入力されたユーザーは存在しません')

    return render_template('users/login.html', form=form) # 'users/'s12-141
# s11-122 ログイン用view関数の追加 end

# s11-127 ログアウトの実装 start
@users.route('/logout') # 'users's12-141
@login_required # s11-128 未ログインユーザーからの保護
def logout():
    logout_user()
    return redirect(url_for('users.login')) # 'users.'s12-141
# s11-127 ログアウトの実装 end

@users.route('/register', methods=['GET','POST']) # 'users's12-141
@login_required # s11-128 未ログインユーザーからの保護
def register():
    form = RegistrationForm()
    # s11-131 権限制御３ start
    if not current_user.is_administrator():
        abort(403)
    # s11-131 権限制御３ end
    if form.validate_on_submit():
        #s10-99ユーザー登録ページの変更 start
        # session['email'] = form.email.data
        # session['username'] = form.username.data
        # session['password'] = form.password.data
        user = User(email=form.email.data, username=form.username.data, password=form.password.data, administrator="0") # s11-125でpassword_hashからpasswordに変更
        db.session.add(user)
        db.session.commit()
        #s10-99ユーザー登録ページの変更 end
        flash('ユーザーが登録されました')
        return redirect(url_for('users.user_maintenance')) # 'users.'s12-141
    return render_template('users/register.html', form=form) # 'users/'s12-141

#s10-102ページネーション１
@users.route('/user_maintenance') # 'users's12-141
@login_required # s11-128 未ログインユーザーからの保護
def user_maintenance():
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.id).paginate(page=page, per_page=10)
    return render_template('users/user_maintenance.html', users=users)

# s10-108 実践７更新用view関数の追加 start
@users.route('/<int:user_id>/account', methods=['GET', 'POST']) # 'users's12-141
@login_required # s11-128 未ログインユーザーからの保護
def account(user_id):
    user = User.query.get_or_404(user_id)
    # s11-132 権限制御４ start
    if user.id != current_user.id and not current_user.is_administrator():
        abort(403)
    # s11-132 権限制御４ end
    form = UpdateUserForm(user_id)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        if form.password.data:
            user.password = form.password.data #s11-127でpassword_hashからpasswordに変更
        db.session.commit()
        flash('ユーザーアカウントが更新されました')
        return redirect(url_for('users.user_maintenance')) # 'users.'s12-141
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
    return render_template('users/account.html', form=form) # 'users/'s12-141
# s10-108 実践７更新用view関数の追加 end

# s10-112 実践11削除用view関数の追加 start
@users.route('/<int:user_id>/delete', methods=['GET', 'POST']) # 'users's12-141
@login_required # s11-128 未ログインユーザーからの保護
def delete_user(user_id):
    user =User.query.get_or_404(user_id)
    # s11-133 権限制御５：ユーザー削除の制限設定 start
    if not current_user.is_administrator():
        abort(403)
    if user.is_administrator():
        flash('管理者は削除できません')
        return redirect(url_for('users.account', user_id=user_id)) # 'users.'s12-141
    # s11-133 権限制御５：ユーザー削除の制限設定 end
    db.session.delete(user)
    db.session.commit()
    flash('ユーザーアカウントが削除されました')
    return redirect(url_for('users.user_maintenance')) # 'users.'s12-141
# s10-112 実践11削除用view関数の追加 end

# s15-210 ユーザー管理ページ(ブログ投稿数)３：view関数の追加 start
@users.route('/<int:user_id>/user_posts')
@login_required
def users_posts(user_id):
    form = BlogSearchForm()
    # ユーザーの取得
    user = User.query.filter(id=user_id).first_or_404()
    
    # ブログ記事の取得
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.id.desc()).paginate(page=page, per_page=10)

    # 最新記事の取得
    recent_blog_posts = BlogPost.query.filter_by(user_id=user_id).order_by(BlogPost.id.desc()).limit(5).all()

    # カテゴリの取得
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()

    return render_template('index.html', blog_posts=blog_posts, recent_blog_posts=recent_blog_posts, blog_categories=blog_categories, user=user, form=form)
# s15-210 ユーザー管理ページ(ブログ投稿数)３：view関数の追加 end