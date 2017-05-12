from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)


# Form Search
@app.route('/')
def form():
    return render_template('form_submit.html')


# Result List
@app.route('/result', methods=['POST'])
def result():
    author=request.form['author']
    genre=request.form['genre']
    return render_template('form_action.html', author=author, genre=genre)


if __name__ == '__main__':
    app.run()