from flask_wtf import FlaskForm # s13-153
from wtforms import StringField, SubmitField, ValidationError, TextAreaField, SelectField # 'StringField, SubmitField, ValidationError's13-153, 'TextAreaField, SelectField's14-167
from wtforms.validators import DataRequired, Email # 'DataRequired's13-153, 'Email's16-217
from company_blog.models import BlogCategory # 'BlogCategory's13-153
from flask_wtf.file import FileField, FileAllowed # 'FileField, FileAllowed's14-167

# s13-153 カテゴリ管理ページ３：フォームの追加 start
class BlogCategoryForm(FlaskForm):
    category = StringField('カテゴリ名', validators=[DataRequired()])
    submit = SubmitField('保存')

    def validate_category(self, field):
        if BlogCategory.query.filter_by(category=field.data).first():
            raise ValidationError('入力されたカテゴリ名は既に使われています。')
# s13-153 カテゴリ管理ページ３：フォームの追加 end

# s13-159 カテゴリ更新ページ３：フォームの追加 start
class UpdateCategoryForm(FlaskForm):
    category = StringField('カテゴリ名', validators=[DataRequired()])
    submit = SubmitField('更新')

    def __init__(self, blog_category_id, *args, **kwargs):
        super(UpdateCategoryForm, self).__init__(*args, **kwargs)
        self.id = blog_category_id

    def validate_category(self, field):
        if BlogCategory.query.filter_by(category=field.data).first():
            raise ValidationError('入力されたカテゴリ名は既に使われています。')
# s13-159 カテゴリ更新ページ３：フォームの追加 end

# s14-167 ブログ投稿ページ３：フォームの追加 start
class BlogPostForm(FlaskForm):
    title = StringField('タイトル', validators=[DataRequired()])
    category = SelectField('カテゴリ', coerce=int)
    summary = StringField('要約', validators=[DataRequired()])
    text = TextAreaField('本文', validators=[DataRequired()])
    picture = StringField('アイキャッチ画像', validators=[FileAllowed(['jpg', 'png'])]) # 'StringField'に変更s17-262
    submit = SubmitField('投稿')

    # カテゴリ項目の設定
    def _set_category(self):
        blog_categories = BlogCategory.query.all()
        self.category.choices = [(blog_category.id, blog_category.category) for blog_category in blog_categories]

    # フォームの初期化
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_category() # カテゴリ項目の設定を呼び出す
# s14-167 ブログ投稿ページ３：フォームの追加 end

# s15-192  ホームページ３：フォームの追加 start
class BlogSearchForm(FlaskForm):
    searchtext = StringField('検索テキスト', validators=[DataRequired()])
    submit = SubmitField('検索')
# s15-192  ホームページ３：フォームの追加 end

# s16-217 お問い合わせページ５：演習②フォームの追加【解答】 start
class InquiryForm(FlaskForm):
    name = StringField('お名前（必須）', validators=[DataRequired()])
    email = StringField('メールアドレス（必須）', validators=[DataRequired(), Email(message='正しいメールアドレスを入力してください')])
    title = StringField('題名')
    text = TextAreaField('メッセージ本文（必須）', validators=[DataRequired()])
    submit = SubmitField('送信')
# s16-217 お問い合わせページ５：演習②フォームの追加【解答】 end