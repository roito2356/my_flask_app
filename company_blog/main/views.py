from flask import Blueprint, render_template, request, url_for, redirect, flash, abort # 'Blueprint's13-148, 'render_template, request, url_for, redirect, flash's13-154, 'abort's13-160
from flask_login import login_required, current_user # 'login_required's13-154, 'current_user's13-160
from company_blog.models import BlogCategory, BlogPost, Inquiry # 'BlogCategory's13-154, 'BlogPost's14-169, 'Inquiry's16-219
from company_blog.main.forms import BlogCategoryForm, UpdateCategoryForm, BlogPostForm, BlogSearchForm, InquiryForm # 'BlogCategoryForm's13-154, 'UpdateCategoryForm's13-160, 'BlogPostForm's14-169, 'BlogSearchForm's15-193, 'InquiryForm's16-219
from company_blog import db # s13-154
from company_blog.main.image_handler import add_featured_image # s14-169

main = Blueprint('main', __name__) # s13-148 Blueprintの基本設定

# s13-154 カテゴリ管理ページ４：view関数の追加 start
@main.route('/category_maintenance', methods=['GET', 'POST'])
@login_required
def category_maintenance():
    page = request.args.get('page', 1, type=int)
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).paginate(page=page, per_page=10)
    form = BlogCategoryForm()
    if form.validate_on_submit():
        blog_category = BlogCategory(category=form.category.data)
        db.session.add(blog_category)
        db.session.commit()
        flash('ブログカテゴリが追加されました')
        return redirect(url_for('main.category_maintenance'))
    elif form.errors:
        form.category.data = ""
        flash(form.errors['category'][0])
    return render_template('category_maintenance.html', blog_categories=blog_categories, form=form)
# s13-154 カテゴリ管理ページ４：view関数の追加 end

# s13-160 カテゴリ更新ページ４：view関数の追加 start
@main.route('/<int:blog_category_id>/blog_category', methods=['GET', 'POST'])
@login_required
def blog_category(blog_category_id):
    if not current_user.is_administrator():
        abort(403)
    blog_category = BlogCategory.query.get_or_404(blog_category_id)
    form = UpdateCategoryForm(blog_category_id)
    if form.validate_on_submit():
        blog_category.category = form.category.data
        db.session.commit()
        flash('ブログカテゴリが更新されました')
        return redirect(url_for('main.category_maintenance'))
    elif request.method == 'GET':
        form.category.data = blog_category.category
    return render_template('blog_category.html', form=form)

@main.route('/<int:blog_category_id>/delete_category', methods=['GET', 'POST'])
@login_required
def delete_category(blog_category_id):
    if not current_user.is_administrator():
        abort(403)
    blog_category = BlogCategory.query.get_or_404(blog_category_id)
    db.session.delete(blog_category)
    db.session.commit()
    flash('ブログカテゴリが削除されました')
    return redirect(url_for('main.category_maintenance'))
# s13-160 カテゴリ更新ページ４：view関数の追加 end

# s14-169 ブログ投稿ページ５：view関数の追加 start
@main.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = BlogPostForm()
    if form.validate_on_submit():
        # s16-262 完成版Webアプリの変更：画像設定1 start
        # if form.picture.data:
        #     pic = add_featured_image(form.picture.data)
        # else:
        #     pic = ''
        # s16-262 完成版Webアプリの変更：画像設定1 end
        blog_post = BlogPost(title=form.title.data, text=form.text.data, featured_image=form.picture.data, user_id=current_user.id, category_id=form.category.data, summary=form.summary.data) # 'form.picture.data'に変更
        db.session.add(blog_post)
        db.session.commit()
        flash('ブログ投稿が作成されました')
        return redirect(url_for('main.blog_maintenance')) # 'blog_maintenance's14-174
    return render_template('create_post.html', form=form)
# s14-169 ブログ投稿ページ５：view関数の追加 end

# s14-174 ブログ管理ページ３：view関数の追加 start
@main.route('/blog_maintenance')
@login_required
def blog_maintenance():
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.id.desc()).paginate(page=page, per_page=10)
    return render_template('blog_maintenance.html', blog_posts=blog_posts)
# s14-174 ブログ管理ページ３：view関数の追加 end

# s14-180 ブログ詳細ページ３：view関数の追加 start
@main.route('/<int:blog_post_id>/blog_post')
def blog_post(blog_post_id):
    # s15-203 ブログ詳細ページ(サイドバー)２：view関数の追加 start
    form = BlogSearchForm()
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    # 最新記事の取得
    recent_blog_posts = BlogPost.query.order_by(BlogPost.id.desc()).limit(5).all()

    # カテゴリの取得
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()

    return render_template('blog_post.html', post=blog_post, recent_blog_posts=recent_blog_posts, blog_categories=blog_categories, form=form)
    # s15-203 ブログ詳細ページ(サイドバー)２：view関数の追加 end
# s14-180 ブログ詳細ページ３：view関数の追加 end

# ｓ14-181 ブログ削除機能２：view関数の追加 start
@main.route('/<int:blog_post_id>/delete_post', methods=['GET', 'POST'])
@login_required
def delete_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)
    db.session.delete(blog_post)
    db.session.commit()
    flash('ブログ投稿が削除されました')
    return redirect(url_for('main.blog_maintenance'))
# s14-181 ブログ削除機能２：view関数の追加 end

# s14-187 ブログ更新機能２：view関数の追加 start
@main.route('/<int:blog_post_id>/update_post', methods=['GET', 'POST'])
@login_required
def update_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)
    form = BlogPostForm()
    if form.validate_on_submit():
        blog_post.title = form.title.data
        # s16-262 完成版Webアプリの変更：画像設定1 start
        # if form.picture.data:
        #     blog_post.featured_image = add_featured_image(form.picture.data)
        blog_post.featured_image = form.picture.data
        # s16-262 完成版Webアプリの変更：画像設定1 end
        blog_post.text = form.text.data
        blog_post.summary = form.summary.data
        blog_post.category_id = form.category.data
        db.session.commit()
        flash('ブログ投稿が更新されました')
        return redirect(url_for('main.blog_post', blog_post_id=blog_post.id))
    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.picture.data = blog_post.featured_image
        form.text.data = blog_post.text
        form.summary.data = blog_post.summary
        form.category.data = blog_post.category_id
    return render_template('create_post.html', form=form)
# s14-187 ブログ更新機能２：view関数の追加 end

# s15-193  ホームページ４：view関数の追加 start
@main.route('/')
def index():
    form = BlogSearchForm()
    # ブログ記事の取得
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.id.desc()).paginate(page=page, per_page=10)

    # 最新記事の取得
    recent_blog_posts = BlogPost.query.order_by(BlogPost.id.desc()).limit(5).all()

    # カテゴリの取得
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()

    return render_template('index.html', blog_posts=blog_posts, recent_blog_posts=recent_blog_posts, blog_categories=blog_categories, form=form)
# s15-193  ホームページ４：view関数の追加 end

# s15-197 ブログ検索機能２：view関数の追加 start
@main.route('/search', methods=['GET', 'POST'])
def search():
    form = BlogSearchForm()
    searchtext = ""
    if form.validate_on_submit():
        searchtext = form.searchtext.data
    elif request.method == 'GET':
        form.searchtext.data = ""
    # ブログ記事の取得
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.filter((BlogPost.text.contains(searchtext)) | (BlogPost.title.contains(searchtext)) | (BlogPost.summary.contains(searchtext))).order_by(BlogPost.id.desc()).paginate(page=page, per_page=10)

    # 最新記事の取得
    recent_blog_posts = BlogPost.query.order_by(BlogPost.id.desc()).limit(5).all()

    # カテゴリの取得
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()

    return render_template('index.html', blog_posts=blog_posts, recent_blog_posts=recent_blog_posts, blog_categories=blog_categories, form=form, searchtext=searchtext)
# s15-197 ブログ検索機能２：view関数の追加 end

# s15-200 カテゴリ別ブログ照会機能２：view関数の追加 start
@main.route('/<int:blog_category_id>/category_posts')
def category_posts(blog_category_id):
    form = BlogSearchForm()

    # カテゴリ名の取得
    blog_category = BlogCategory.query.filter_by(id=blog_category_id).first_or_404()

    # ブログ記事の取得
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.filter_by(category_id=blog_category_id).order_by(BlogPost.id.desc()).paginate(page=page, per_page=10)

    # 最新記事の取得
    recent_blog_posts = BlogPost.query.order_by(BlogPost.id.desc()).limit(5).all()

    # カテゴリの取得
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()

    return render_template('index.html', blog_posts=blog_posts, recent_blog_posts=recent_blog_posts, blog_categories=blog_categories, blog_category=blog_category, form=form)
# s15-200 カテゴリ別ブログ照会機能２：view関数の追加 end

# s16-219 お問い合わせページ７：演習③view関数の追加【解答】 start
@main.route('/inquiry', methods=['GET', 'POST'])
def inquiry():
    form = InquiryForm()
    if form.validate_on_submit():
        inquiry = Inquiry(name=form.name.data,
                            email=form.email.data,
                            title=form.title.data,
                            text=form.text.data)
        db.session.add(inquiry)
        db.session.commit()
        flash('お問い合わせが送信されました')
        return redirect(url_for('main.inquiry'))
    return render_template('inquiry.html', form=form)
# s16-219 お問い合わせページ７：演習③view関数の追加【解答】 end

# s16-227 お問い合わせ管理ページ５：演習2view関数の追加【解答】 start
@main.route('/inquiry_maintenance')
@login_required
def inquiry_maintenance():
    page = request.args.get('page', 1, type=int)
    inquiries = Inquiry.query.order_by(Inquiry.id.desc()).paginate(page=page, per_page=10)
    return render_template('inquiry_maintenance.html', inquiries=inquiries)
# s16-227 お問い合わせ管理ページ５：演習2view関数の追加【解答】 end

# s16-233 お問い合わせ詳細ページ３：演習①view関数の追加【解答】 start
@main.route('/<int:inquiry_id>/display_inquiry')
@login_required
def display_inquiry(inquiry_id):
    inquiry = Inquiry.query.get_or_404(inquiry_id)
    form = InquiryForm()
    form.name.data = inquiry.name
    form.email.data = inquiry.email
    form.title.data = inquiry.title
    form.text.data = inquiry.text
    return render_template('inquiry.html', form=form, inquiry_id=inquiry_id)
# s16-233 お問い合わせ詳細ページ３：演習①view関数の追加【解答】 end

# s16-240 お問い合わせ削除機能３：演習①view関数の追加【解答】 start
@main.route('/<int:inquiry_id>/delete_inquiry', methods=['GET', 'POST'])
@login_required
def delete_inquiry(inquiry_id):
    inquiries = Inquiry.query.get_or_404(inquiry_id)
    if not current_user.is_administrator():
        abort(403)
    db.session.delete(inquiries)
    db.session.commit()
    flash('お問い合わせが削除されました')
    return redirect(url_for('main.inquiry_maintenance'))
# s16-240 お問い合わせ削除機能３：演習①view関数の追加【解答】 end

# s16-246 会社情報ページ３：view関数の追加 start
@main.route('/info')
def info():
    return render_template('info.html')
# s16-246 会社情報ページ３：view関数の追加 end