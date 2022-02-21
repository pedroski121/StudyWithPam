from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


print(__name__)
if __name__ == '__main__':
    app.run(debug=True)
