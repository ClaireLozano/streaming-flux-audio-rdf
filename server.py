from flask import Flask
from flask import render_template
from flask import request

from services import Services
import os

app = Flask(__name__)

# Initialisation du graphe et peuplement
service = Services()

RACINE = "/Users/thomas/Documents/Master/Digital\ Content\ Broadcasting/untitled"


@app.route("/start_song", methods=['POST'])
def start_wav_function():
    print('start song')
    os.system("python " + RACINE + "/streaming/client_web.py localhost " + request.form['song'] + " &")
    return "start"


# Form Search
@app.route('/')
def form():
    return render_template('form_submit.html', genres=service.request_genre_sparql())


# Result List
@app.route('/result', methods=['POST'])
def result():
    author = request.form['author']
    genre = request.form['genre']
    results = service.request_sparql(author, genre)
    return render_template('form_action.html', author=author, genre=genre, results=results,
                           start_wav_function=start_wav_function)


if __name__ == '__main__':
    app.run()
