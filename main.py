from flask import Response, redirect, render_template, request, flash, url_for
from sqlalchemy import exc
from model import app, db, Image, Email, Post, User, Comments
# For ensuring the file uploaded is not dangerous
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from form import PostForm
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from flask_login import login_user, LoginManager, login_required, current_user, logout_user

login_manager = LoginManager()
login_manager.init_app(app)


Bootstrap(app)
app.config['CKEDITOR_PKG_TYPE'] = 'basic'
app.config['IMAGE_UPLOADS'] = "static/images"
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]


ckeditor = CKEditor(app)


# checking File types allowed for getting uploaded


def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.split(".")[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

# Error Handler incase the uploaded file is too large


@app.errorhandler(413)
def error413(e):
    return "THE FILE SIZE IS TOO LARGE"


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


@app.context_processor
def inject_user():
    return dict(user_status=current_user.is_authenticated, id=current_user.get_id())


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/articles')
def articles():
    page = request.args.get('page', 1, type=int)
    # all_post_paginate = db.session.query.order_by(Post.id.desc())
    all_articles = Post.query.order_by(
        Post.id.desc()).paginate(page=page, per_page=6)
    return render_template('articles.html', posts=all_articles)


@app.route('/delete-article/<article_id>')
@login_required
def delete_article(article_id):
    article = Post.query.get(article_id)
    current_user_id = int(current_user.get_id())
    article_id = article.author_id

    if article_id == current_user_id:
        db.session.delete(article)
        db.session.commit()
        return redirect(url_for('profile', user_id=current_user_id))
    else:
        return 'Not authorized'


@app.route('/article-content/<id>')
def article_content(id):
    post = Post.query.get(id)
    comments = Comments.query.filter_by(post_id=id).all()
    comment_data = []
    for comment in comments:
        text = comment.comment
        date = comment.date
        author_id = comment.comment_author_id
        user_name = User.query.get(author_id).name.title()
        comment_data.append({
            "comment_text": text,
            "comment_date": date,
            "comment_author": user_name,
            "comment_date": date
        })
    return render_template('article-content.html', post=post, comments=comment_data)


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['pswd']
    user = User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(pwhash=user.password, password=password):
            print('password is correct')
            login_user(user)
            return redirect(url_for('profile', user_id=user.id))
        return "Your password is incorrect"
    return 'Your email address does not exist'


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['POST'])
def register():
    name = request.form["name"]
    email = request.form['email']
    password = request.form['pswd']
    password_hashed = generate_password_hash(
        password=password, method='pbkdf2:sha256', salt_length=8)
    username = request.form['username']
    today = date.today().strftime("%b %d, %Y")
    new_user = User(name=name, email=email,
                    password=password_hashed,
                    username=username,
                    creation_date=today,
                    profile_description='Welcome to my SWP page')
    try:
        db.session.add(new_user)
        db.session.commit()
    except exc.IntegrityError:
        return 'It seems like your email or username already exists'
    finally:
        login_user(new_user)
        print(new_user.id)
    return redirect(url_for('profile', user_id=new_user.id))

# PROFILE PAGE


@app.route('/profile/<user_id>')
def profile(user_id):
    page = request.args.get('page', 1, type=int)
    all_user_post = Post.query.filter_by(
        author_id=user_id).order_by(Post.id.desc()).paginate(page=page, per_page=6)
    user = User.query.filter_by(id=user_id).first()
    user_data = dict(
        name=user.name.title(),
        user_name=user.username,
        creation_date=user.creation_date,
        profile_description=user.profile_description)
    return render_template('profilepage.html', posts=all_user_post, user=user_data, user_id=user_id)


@app.route('/post-article/<user_id>', methods=['GET', 'POST'])
def post_article(user_id):
    author = User.query.get(user_id)
    form = PostForm()
    if form.validate_on_submit():
        course = form.course.data
        topic = form.topic.data
        body = form.body.data
        today = date.today().strftime("%b %d, %Y")
        post_writeup = Post(course=course, topic=topic,
                            body=body, date=today, author=author)
        db.session.add(post_writeup)
        db.session.commit()
        return redirect(url_for('profile', user_id=user_id))
    return render_template('post-article.html', form=form)


# SIGN UP FOR NEWS LETTER ROUTE
@app.route('/email-registration', methods=['GET', 'POST'])
def email_registration():
    if request.method == "POST":
        try:
            email_address = Email(email=request.form["email_address"])
            db.session.add(email_address)
            db.session.commit()
            flash('Signed up for SWP newsletter')
        except exc.IntegrityError:
            flash('Your email address already exists')
    return redirect(url_for('home'))


@app.route("/upload-image/<user_id>", methods=['GET', "POST"])
@login_required
def upload_image(user_id):
    if request.method == 'POST':
        user_profile = User.query.get(user_id)
        if request.files:
            image = request.files['image']
            # TO ENSURE THE FILE UPLOADED HAS A NAME
            if image.filename == "":
                return "No filename"
            elif allowed_image(image.filename):
                # Image is suitable for further processing
                filename = secure_filename(image.filename)
                mimetype = image.mimetype
                # Add Image to database

                if filename or mimetype:

                    query_id = Image.query.filter_by(user_id=user_id).first()
                    if query_id:
                        query_id.mimetype = mimetype
                        query_id.name = filename
                        query_id.img = image.read()
                        query_id.user = user_profile
                        db.session.commit()
                        return redirect(url_for('get_img', id=user_id))

                    else:
                        img = Image(img=image.read(),
                                    mimetype=mimetype, name=filename, user=user_profile)
                        db.session.add(img)
                        db.session.commit()
                        return redirect(url_for('get_img', id=user_id))
                else:
                    return "Bad Upload", 400
            else:
                return "Bad Upload", 400
    return render_template('upload_image.html')


@app.route("/get-image/<int:id>")
def get_img(id):
    image = Image.query.filter_by(user_id=id).first()
    if not image:
        return "Image cannot be found", 404
    return Response(image.img, mimetype=image.mimetype)


@app.route('/description/<user_id>', methods=['GET', 'POST'])
@login_required
def description(user_id):
    user_description = User.query.get(user_id)
    if request.method == 'POST':
        new_description = request.form['description']
        user_description.profile_description = new_description
        db.session.commit()
        return redirect(url_for('profile', user_id=user_id))
    if user_description.profile_description:
        return render_template('description.html', current_description=user_description.profile_description)
    else:
        return render_template('description.html', current_description='Welcome to my SWP page')


@app.route('/comment/<post_id>', methods=['POST'])
@login_required
def comment(post_id):
    comment_text = request.form['comment']
    today = date.today().strftime("%b %d, %Y")
    comment = Comments(comment=comment_text, comment_author_id=current_user.get_id(
    ), post_id=post_id, date=today)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('article_content', id=post_id))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

