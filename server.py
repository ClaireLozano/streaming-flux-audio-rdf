# coding=utf-8
import sys
from flask import Flask
from flask import render_template
from flask import request

from services import Services
import os

# Démarrage de Flask
app = Flask(__name__)

# Initialisation du graphe et peuplement
service = Services()

# Vérification de la présence de l'url racine du projet
if (len(sys.argv) < 1):
    print("Not enough arguments! \n *** Usage: {0} <url_racine_project> ***\n".format(sys.argv[0]))
    sys.exit()

# Attribution de l'url racine avec le paramètre entrant
RACINE = sys.argv[1]


# Route /start_song POST
# Permettre de lancer la musique dont le nom est passé dans l'url
@app.route("/start_song", methods=['POST'])
def start_wav_function():
    os.system("python " + RACINE + "/streaming/client_web.py localhost " + request.form['song'] + " &")
    return "start song"


# Route / GET
# Afficher la page de recherche
@app.route('/')
def form():
    # Création de la vue
    return render_template('form_submit.html', gender=service.request_gender_sparql())


# Route /result
# Afficher la page contenant les résultats de la recherche
@app.route('/result', methods=['POST'])
def result():
    # Récupération des paramètres
    author = request.form['author']
    gender = request.form['gender']

    # Requête SPARQL pour récupérer des résultats
    results = service.request_sparql(author, gender)

    # Création de la vue
    return render_template('form_action.html', author=author, gender=gender, results=results)


# Lancer Flask
if __name__ == '__main__':
    app.run()
