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
import time

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
        framenum_values=settings.framenum_values,
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

    start_time = int(time.time())
    print start_time
    try:
        ws.send(json.dumps({"text": "Resetting usb"}))
        util.usb_resetter.reset_usb(settings.manufacturer)

        ws.send(json.dumps({"text": "Taking %d pics" % num_pics}))
        util.photo.take_photos(num_pics)
    except:
        pass

    filenames = util.photo.get_filenames_of_recent_photos(num_pics, start_time)
    ws.send(json.dumps({"text": "Making %d thumbnails..." % len(filenames)}))

    # make thumbnails
    for current, filename in enumerate(filenames, 1):
        message = "Making thumbnail {current} of {total}".format(
            current=current,
            total=len(filenames)
        )
        ws.send(json.dumps({"text": message}))
        util.photo.make_thumbnail(filename)

        thumbnail_original_pairs = util.photo.get_thumbnail_original_pairs(
            originals=[filename]
        )

        # get the HTML for the recently-taken photo
        ctx = app.test_request_context()
        ctx.push()
        new_thumbnail_html = render_template(
            'photo_container.html',
            thumbnail_original_pairs=thumbnail_original_pairs,
            invisible=True
        )
        ctx.pop()
        ws.send(json.dumps({"new_thumbnail_html": new_thumbnail_html}))


    final_data = {
        "text": "TOOK %d PICTURES" % len(thumbnail_original_pairs)
    }
    ws.send(json.dumps(final_data))
    ws.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
