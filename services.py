import os
import tempfile
import libxmp
import rdflib
from rdflib.plugins.sparql import prepareQuery
from rdflib import Namespace

# encoding=utf8
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class Services:
    def __init__(self):
        self.PATH = os.path.dirname(os.path.realpath(__file__)) + "/FichiersMusicaux/"
        self.EXTENSION = ".wav"
        self.name_space_artist = Namespace("http://ns.adobe.com/xmp/1.0/DynamicMedia/")
        self.g = rdflib.Graph()
        self.list_all_files()

    def read_xmp_metadata(self, file):
        # Read file
        xmpfile = libxmp.XMPFiles(file_path=file, open_forupdate=False)
        # Get XMP from file
        xmp = xmpfile.get_xmp()
        xmp = str(xmp)
        xmp = "<rdf:RDF" + xmp.split("<rdf:RDF", 1)[1]
        xmp = xmp.split("</rdf:RDF>", 1)[0] + "</rdf:RDF>"
        #print xmp
        xmpfile.close_file()
        return xmp

    def import_graph(self, rdf, filename):
        temp = tempfile.NamedTemporaryFile(prefix=filename+'_')
        temp.write(rdf)
        temp.seek(0)
        self.g.load(temp.name)
        #for s, p, o in self.g:
        #    print s, p, o
        temp.close()

    def list_all_files(self):
        print("--- start list_all_files() ---")
        for root, dirs, files in os.walk(self.PATH):
            for name in files:
                if name.endswith(self.EXTENSION):
                    print("--- read_xmp_metadata : " + name + " ---")
                    self.import_graph(self.read_xmp_metadata(root + "/" + name), str(name))
        print("--- end list_all_files() ---")

    def simplify(self, text):
        return text.split("/")[-1]

    def simplify_name_title(self, text):
        return (text.split("/")[-1]).split("_", 1)[0]

    def request_sparql(self, auteur, genre):
        if not auteur:
            q = prepareQuery(
                'SELECT DISTINCT * WHERE { ?s xmpDM:genre "' + genre + '". ?s ?predicate ?object . }',
                initNs={"xmpDM": self.name_space_artist})
        else:
            q = prepareQuery(
                'SELECT DISTINCT * WHERE { ?s xmpDM:artist "' + auteur + '" . ?s xmpDM:genre "' + genre + '". ?s ?predicate ?object . }',
                initNs={"xmpDM": self.name_space_artist})
        dico = {}
        for b, c, d in self.g.query(q):
            # Show result
            #print b, c, d
            # Initialisation d'un tableau contenant les informations d'un nouveau titre de musique
            if dico.get(self.simplify_name_title(str(c))) == None:
                dico[self.simplify_name_title(str(c))] = []
            # Ajout d'information sur lte titre de musique
            dico[self.simplify_name_title(str(c))].append([str(b), self.simplify(str(d))])
        return dico

    def request_genre_sparql(self):
        q = prepareQuery(
            'SELECT DISTINCT ?y WHERE { ?x xmpDM:genre ?y . }',
            initNs={"xmpDM": self.name_space_artist})
        dico = []
        for b in self.g.query(q):
            dico.append(str(b).split("'")[1])
        return dico
