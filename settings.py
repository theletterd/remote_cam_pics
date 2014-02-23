import os
ROOT_DIR =  os.path.abspath(os.path.dirname(__file__)) + '/'
static_dir = ROOT_DIR + 'static'
originals_dir_name = 'originals'
thumbnails_dir_name = 'thumbnails'

originals_dir = static_dir + '/' + originals_dir_name
thumbnails_dir = static_dir + '/' + thumbnails_dir_name

framenum_values = [1, 5, 10, 20]

manufacturer = 'nikon'
