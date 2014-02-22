from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

import util.sass
import util.usb_resetter
import util.photo

import settings
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    if app.debug:
        util.sass.regenerate_scss()

    thumbnail_original_pairs = util.photo.get_thumbnail_original_pairs(limit=30)
    return render_template(
        'index.html',
        thumbnail_original_pairs=thumbnail_original_pairs,
        framenum_values=settings.framenum_values
    )

@app.route('/take_pics', methods=['POST'])
def take_pics():
    num_pics = int(request.form['framenum'])

    assert num_pics in settings.framenum_values

    util.usb_resetter.reset_usb(settings.manufacturer)
    util.photo.take_photos(num_pics)
    util.photo.make_thumbnails(num_pics)

    return jsonify(success=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
