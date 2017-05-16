# coding=utf-8
import os
import tempfile
import libxmp
import rdflib
from rdflib.plugins.sparql import prepareQuery
from rdflib import Namespace
import sys

# Forcer l'UTF-8 pour l'ensemble des traitements
reload(sys)
sys.setdefaultencoding('utf8')


# Classe SERVICES chargée de la création du graphe
# et des requêtes SPARQL
class Services:
    # Constructeur par défaut
    def __init__(self):
        # Déclaration des variables globales
        self.PATH = os.path.dirname(os.path.realpath(__file__)) + "/FichiersMusicaux/"
        self.EXTENSION = ".wav"
        self.name_space_artist = Namespace("http://ns.adobe.com/xmp/1.0/DynamicMedia/")
        self.g = rdflib.Graph()  # Création d'un nouveau graphe
        self.list_all_files()  # Début du peuplement du graphe

    # Lire un fichier audio et récupérer la partie RDF
    def read_xmp_metadata(self, file):
        # Lecture du fichier
        xmpfile = libxmp.XMPFiles(file_path=file, open_forupdate=False)
        # Récupérer le XML
        xmp = str(xmpfile.get_xmp())
        xmp = "<rdf:RDF" + xmp.split("<rdf:RDF", 1)[1]
        xmp = xmp.split("</rdf:RDF>", 1)[0] + "</rdf:RDF>"
        # Fermer le fichier
        xmpfile.close_file()
        # Retourner le contenu RDF
        return xmp

    # Importation d'un RDF dans le graphe
    def import_graph(self, rdf, filename):
        # Génération d'un fichier temporaire intermédiaire
        temp = tempfile.NamedTemporaryFile(prefix=filename + '_')
        temp.write(rdf)
        # Etape importante! Remettre la tête de lecture au début.
        temp.seek(0)
        # Envoi du fichier de le graphe
        self.g.load(temp.name)
        # Afficher les informations contenus dans le graphe
        # for s, p, o in self.g:
        #    print s, p, o
        # Destruction du fichier temporaire
        temp.close()

    # Lister tous les fichiers de musique
    def list_all_files(self):
        print("--- start list_all_files() ---")
        # Parcours du dossier FichiersMusicaux
        for root, dirs, files in os.walk(self.PATH):
            for name in files:
                # Correspondace avec un .wav
                if name.endswith(self.EXTENSION):
                    print("--- read_xmp_metadata : " + name + " ---")
                    # Extraction des méta-données et envoi de le graphe
                    self.import_graph(self.read_xmp_metadata(root + "/" + name), str(name))
        print("--- end list_all_files() ---")

    # Ne garder que la partie de description de l'information
    # namespace/../../../Rating  ne garder que le Rating
    def simplify(self, text):
        return text.split("/")[-1]

    # Les noeuds principaux contiennent le path du fichier provisoire
    # ne garder uniquement la partie indiquant le nom de la chanson
    def simplify_name_title(self, text):
        return (text.split("/")[-1]).split("_", 1)[0]

    # Effectuer une requête SPARQL tenant compte de l'auteur et du genre de la musique
    def request_sparql(self, auteur, gender):
        if not auteur:
            q = prepareQuery(
                'SELECT DISTINCT * WHERE { ?s xmpDM:genre "' + gender + '". ?s ?predicate ?object . }',
                initNs={"xmpDM": self.name_space_artist})
        else:
            q = prepareQuery(
                'SELECT DISTINCT * WHERE { ?s xmpDM:artist "' + auteur + '" . ?s xmpDM:genre "' + gender + '". ?s ?predicate ?object . }',
                initNs={"xmpDM": self.name_space_artist})
        # Préparation du résultat retourné
        resultList = {}
        for subject, predicate, object in self.g.query(q):
            # Initialisation d'un tableau contenant les informations d'un nouveau titre de musique
            if resultList.get(self.simplify_name_title(str(predicate))) == None:
                resultList[self.simplify_name_title(str(predicate))] = []
            # Ajout d'information sur les titres musicaux
            resultList[self.simplify_name_title(str(predicate))].append([str(subject), self.simplify(str(object))])
        return resultList

    # Effectuer une requête permettant de récupérer les genres musicaux
    def request_genre_sparql(self):
        q = prepareQuery(
            'SELECT DISTINCT ?y WHERE { ?x xmpDM:genre ?y . }',
            initNs={"xmpDM": self.name_space_artist})
        resultList = []
        for b in self.g.query(q):
            resultList.append(str(b).split("'")[1])
        return resultList
