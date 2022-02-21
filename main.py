from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/articles')
def articles():
    return render_template('articles.html')


@app.route('/article-content')
def article_content():
    return render_template('article-content.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/our-story')
def story():
    return 'OUR STORY'


@app.route('/donate')
def donate():
    return 'Donate'


print(__name__)
if __name__ == '__main__':
    app.run(debug=True)
