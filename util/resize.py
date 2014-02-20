#!/usr/bin/python

from optparse import OptionParser
from PIL import Image

class CLImageResizer(object):

    def _init_parser(self):
        usage = "usage: %prog [options] path_to_file"
        parser = OptionParser()

        parser.add_option("-o", "--output-directory", dest="output_directory", help="place output image into DIR", metavar="DIR", default="./")
        parser.add_option("-s", "--shrink", dest="shrink_factor", help="Shrink image by a factor of FACTOR", metavar="FACTOR", default=10)

        (options, args) = parser.parse_args()

        if not args:
            parser.error("Must supply file to be resized")
        if len(args) != 1:
            parser.error("invalid number of arguments")

        return options, args

    def __init__(self):
        options, args = self._init_parser()

        self.output_directory = options.output_directory
        self.shrink_factor = options.shrink_factor
        path_to_file = args[0]
        self.resize_image(path_to_file)

    def resize_image(self, path_to_file):
        img = Image.open(path_to_file)
        new_size = [dimension / int(self.shrink_factor) for dimension in img.size]
        img.thumbnail(new_size)
        filename = path_to_file.split('/')[-1]
        path = "{output_dir}/{filename}".format(output_dir=self.output_directory, filename=filename)
        img.save(path)
        print "Thumbnail saved as %s" % path


if __name__ == '__main__':
    resizer = CLImageResizer()
