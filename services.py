import os
import tempfile
import libxmp
import rdflib
from rdflib.plugins.sparql import prepareQuery
from rdflib import Namespace


class Services:
    def __init__(self):
        self.PATH = "/Users/thomas/Documents/Master/Digital Content Broadcasting/untitled/FichiersMusicaux/"
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
        print xmp
        xmpfile.close_file()
        return xmp

    def import_graph(self, rdf):
        temp = tempfile.NamedTemporaryFile()
        temp.write(rdf)
        temp.seek(0)
        self.g.load(temp.name)
        for s, p, o in self.g:
            print s, p, o
        temp.close()

    def list_all_files(self):
        print("--- start list_all_files() ---")
        for root, dirs, files in os.walk(self.PATH):
            for name in files:
                if name.endswith(self.EXTENSION):
                    print("--- read_xmp_metadata : " + name + " ---")
                    self.import_graph(self.read_xmp_metadata(root + "/" + name))
        print("--- end list_all_files() ---")

    def request_sparql(self, auteur, genre):
        q = prepareQuery(
            'SELECT * WHERE { ?s xmpDM:artist "' + auteur + '" . ?s xmpDM:genre "' + genre + '". ?s ?predicate ?object . }',
            initNs={"xmpDM": self.name_space_artist})
        # Show result
        a = []
        for b, c, d in self.g.query(q):
            print b, c, d
            a.append([b, c, d])
        return a
