from flask import Response, redirect, render_template, request, flash, url_for
from sqlalchemy import exc
from model import app, db, Image, Email, Post
# For ensuring the file uploaded is not dangerous
from werkzeug.utils import secure_filename
from form import PostForm
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor

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


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/articles')
def articles():
    return render_template('articles.html')


@app.route('/article-content/<id>')
def article_content(id):
    post = Post.query.get(id)
    return render_template('article-content.html', post=post)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/profile')
def profile():
    all_user_post = db.session.query(Post).all()
    return render_template('profilepage.html', posts=all_user_post)


@app.route('/post-article', methods=['GET', 'POST'])
def post_article():
    form = PostForm()
    if form.validate_on_submit():
        course = form.course.data
        topic = form.topic.data
        body = form.body.data
        post_writeup = Post(course=course, topic=topic, body=body)
        db.session.add(post_writeup)
        db.session.commit()
        return redirect(url_for('profile'))
    return render_template('post-article.html', form=form)


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


@app.route("/upload-image", methods=["POST"])
def upload_image():
    if request.files:
        image = request.files['image']
        # TO ENSURE THE FILE UPLOADED HAS A NAME
        print(image.filename)
        if image.filename == "":
            return "No filename"
        if allowed_image(image.filename):
            # Image is suitable for further processing
            filename = secure_filename(image.filename)
            mimetype = image.mimetype
            # Add Image to database
            if filename or mimetype:
                img = Image(img=image.read(),
                            mimetype=mimetype, name=filename)
                db.session.add(img)
                db.session.commit()
                return redirect(url_for('get_img',id=7))
            else:
                return "Bad Upload", 400


# @app.route('/get-image/<int:id>')
# def get_img(id):
#     img = Image.query.filter_by(id=id).first()
#     if not img:
#         return 'Img Not Found!', 404
#     return Response(img.img, mimetype=img.mimetype)


# def upload_image():
#     if request.method == "POST":
#         pic = request.files['image']
#         if not pic:
#             return 'No pic uploaded!', 400

#         filename = secure_filename(pic.filename)
#         mimetype = pic.mimetype
#         if not filename or not mimetype:
#             return 'Bad upload!', 400

#         img = Image(img=pic.read(), name=filename, mimetype=mimetype)
#         db.session.add(img)
#         db.session.commit()

#         return 'Img Uploaded!', 200
#     return render_template('upload_image.html')


@app.route("/get-image/<int:id>")
def get_img(id):
    image = Image.query.get(id)
    if not image:
        return "Image cannot be found", 404
    return Response(image.img, mimetype=image.mimetype)


if __name__ == '__main__':
    app.run(debug=True)
