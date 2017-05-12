import os
import tempfile
import libxmp
import rdflib
from rdflib.plugins.sparql import prepareQuery
from rdflib import Namespace

PATH = "../FichiersMusicaux/"
EXTENSION = ".wav"
g = rdflib.Graph()
name_space_artist = Namespace("http://ns.adobe.com/xmp/1.0/DynamicMedia/")


def read_xmp_metadata(file):
    # Read file
    xmpfile = libxmp.XMPFiles(file_path=file, open_forupdate=False)
    # Get XMP from file
    xmp = xmpfile.get_xmp()
    xmp = str(xmp)
    xmp = "<rdf:RDF" + xmp.split("<rdf:RDF",1)[1]
    xmp = xmp.split("</rdf:RDF>", 1)[0] + "</rdf:RDF>"
    print xmp
    xmpfile.close_file()
    return xmp


def list_all_files():
    print("--- start list_all_files() ---")
    for root, dirs, files in os.walk(PATH):
        for name in files:
            if name.endswith(EXTENSION):
                print("--- read_xmp_metadata : " + name + " ---")
                import_graph(read_xmp_metadata(root + "/" + name))
    print("--- end list_all_files() ---")


def import_graph(rdf):
    temp = tempfile.NamedTemporaryFile()
    temp.write(rdf)
    temp.seek(0)
    g.load(temp.name)
    for s, p, o in g:
        print s, p, o
    temp.close()


def request_sparql(auteur, genre):
    list_all_files()
    q = prepareQuery('SELECT * WHERE { ?s xmpDM:artist "' + auteur + '" . ?s xmpDM:genre "' + genre + '". ?s ?predicate ?object . }', initNs={"xmpDM": name_space_artist})
    #Show result
    #for row in g.query(q):
    #    print row
    return g.query(q)