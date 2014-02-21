from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from util.util import get_thumbnail_original_pairs
from util.util import take_photos_and_make_thumbnails

import settings

import os

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    thumbnail_original_pairs = get_thumbnail_original_pairs(limit=30)
    return render_template(
        'index.html',
        thumbnail_original_pairs=thumbnail_original_pairs,
        framenum_values=settings.framenum_values
    )

@app.route('/take_pics', methods=['POST'])
def take_pics():
    num_pics = int(request.form['framenum'])

    assert num_pics in settings.framenum_values
    
    take_photos_and_make_thumbnails(num_pics)

    # ok this is where we do the business as it were.
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
