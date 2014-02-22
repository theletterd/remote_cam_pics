import os
import settings
from scss import Scss

SASS_ASSETS_DIR = settings.ROOT_DIR + 'assets/scss'
SASS_OUTPUT_DIR = settings.ROOT_DIR + 'static/css'

def get_scss_filenames():
    sass_files = []
    for root, _, filenames in os.walk(SASS_ASSETS_DIR):
        for filename in filenames:
            _, extension = os.path.splitext(filename)
            if extension in ('.scss', '.sass'):
                sass_files.append(os.path.join(root, filename))
    return sass_files

def get_output_filename(filename):
    filename = filename.replace(SASS_ASSETS_DIR, SASS_OUTPUT_DIR)
    filename, _ = os.path.splitext(filename)
    return filename + '.css'

def regenerate_scss():
    compiler = Scss()
    filenames = get_scss_filenames()
    for filename in filenames:
        with open(filename, 'r') as f:
            raw_sass = ''.join(f.readlines())
        output = compiler.compile(raw_sass)
        output_filename = get_output_filename(filename)
        with open(output_filename, 'w') as f:
            f.write(output)
