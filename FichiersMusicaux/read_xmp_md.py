import libxmp
import sys

for arg in sys.argv:
	# Read file
	xmpfile = libxmp.XMPFiles( file_path=arg , open_forupdate=False)

	# Get XMP from file
	xmp = xmpfile.get_xmp()
	print 'XMP metadata = ', xmp

	xmpfile.close_file()



