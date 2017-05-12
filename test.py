import libxmp
from libxmp import *
from libxmp import consts

xmpfile = XMPFiles(
    file_path="./files/image.jpg",
    open_forupdate=True)

# Get XMP from file.
xmp = xmpfile.get_xmp()

# Print the property dc:format
print(xmp)
