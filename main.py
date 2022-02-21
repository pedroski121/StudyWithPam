from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/our-story')
def story():
    return 'OUR STORY'


@app.route('/login')
def login():
    return 'Login'

@app.route('/articles')
def articles():
    return 'Articles'

@app.route('/donate')
def donate():
    return 'Donate'



print(__name__)
if __name__ == '__main__':
    app.run(debug=True)
