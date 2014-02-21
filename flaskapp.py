from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from util.util import get_recently_created_filenames
from util.util import reset_usb

import os

app = Flask(__name__)

FRAMENUM_VALUES = [1, 5, 10, 20]

@app.route('/', methods=['GET'])
def index():
    thumbnail_filenames = get_recently_created_filenames('static/thumbs', limit=30)
    thumbnails = [filename.replace('static/', '', 1) for filename in thumbnail_filenames]
    return render_template(
        'index.html',
        thumbnails=thumbnails,
        framenum_values=FRAMENUM_VALUES
    )

@app.route('/take_pics', methods=['POST'])
def take_pics():
    pics_to_take = int(request.form['framenum'])

    assert pics_to_take in FRAMENUM_VALUES
    
    reset_usb('nikon')
    os.system('util/take_ten_pics ./static/originals/ ./static/thumbs/ %d' % pics_to_take)
    # ok this is where we do the business as it were.
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
