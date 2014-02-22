activate_this = '/home/duncan/programming/remote_cam_pics/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.insert(0, '/home/duncan/programming/remote_cam_pics')
from flaskapp import app as application