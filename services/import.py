import os
import libxmp
import rdflib

PATH = "../FichiersMusicaux/"
EXTENSION = ".wav"


def read_xmp_metadata(file):
    # Read file
    xmpfile = libxmp.XMPFiles(file_path=file, open_forupdate=False)
    # Get XMP from file
    xmp = xmpfile.get_xmp()
    print xmp
    xmpfile.close_file()


def list_all_files():
    print("--- start list_all_files() ---")
    for root, dirs, files in os.walk(PATH):
        for name in files:
            if name.endswith(EXTENSION):
                print("--- read_xmp_metadata : " + name + " ---")
                read_xmp_metadata(root + "/" + name)
    print("--- end list_all_files() ---")


def import_graph(rdf):
    g = rdflib.Graph()
    g.load(rdf)
    for s, p, o in g:
        print s, p, o



list_all_files()
