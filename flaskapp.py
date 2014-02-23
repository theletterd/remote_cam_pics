from flask import Flask
from flask import jsonify
from flask import json
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from flask_sockets import Sockets

import util.sass
import util.usb_resetter
import util.photo

import settings
import os

app = Flask(__name__)
sockets = Sockets(app)

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

@sockets.route('/ws_take_pics')
def ws_take_pics(ws):
    message = json.loads(ws.receive())
    num_pics = int(message['num_pics'])

    assert num_pics in settings.framenum_values

    try:
        ws.send(json.dumps({"message":"Resetting usb"}))
        util.usb_resetter.reset_usb(settings.manufacturer)

        ws.send(json.dumps({"message":"Taking %d pics" % num_pics}))
        util.photo.take_photos(num_pics)

        ws.send(json.dumps({"message":"Making thumbnails"}))
        util.photo.make_thumbnails(num_pics)
    except:
        ws.send(json.dumps({"message":":("}))
    ws.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
