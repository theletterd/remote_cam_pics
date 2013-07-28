#!/usr/bin/python

from optparse import OptionParser
from PIL import Image


usage = "usage: %prog [options] filename"
parser = OptionParser()

parser.add_option("-o", "--output-directory", dest="output_dir", help="place output image into DIR", metavar="DIR", default="./")
parser.add_option("-s", "--shrink", dest="shrink_factor", help="Shrink image by a factor of FACTOR", metavar="FACTOR", default=10)

(options, args) = parser.parse_args()

if not args:
    parser.error("Must supply file to be resized")
if len(args) != 1:
    parser.error("invalid number of arguments")

filename = args[0]
output_dir = options.output_dir
shrink_factor = options.shrink_factor

img = Image.open(filename)
new_size = [dimension / int(shrink_factor) for dimension in img.size]
img.thumbnail(new_size)
path = "{output_dir}/{filename}".format(output_dir=output_dir, filename=filename)
img.save(path)
print "Thumbnail saved as %s" % path

