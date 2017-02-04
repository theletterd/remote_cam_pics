from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask import url_for
import flask_socketio as socketio
from flask_socketio import SocketIO

import util.sass
import util.usb_resetter
import util.photo
import settings

import os
import logging
import time


app = Flask(__name__)
socketio_app = SocketIO(app)
log = logging.getLogger(__file__)
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(msg)s")


@app.route('/', methods=['GET'])
def index():
    # make this a deploy script or something
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


@socketio_app.on('take_pics')
def ws_take_pics(message):
    log.debug(message)
    num_pics = int(message['num_pics'])

    assert num_pics in settings.framenum_values

    start_time = int(time.time())
    log.debug(start_time)
    try:
        socketio.emit('update_text', {"text": "Resetting usb"})
        util.usb_resetter.reset_usb(settings.manufacturer)

        socketio.emit('update_text', {"text": "Taking %d pics" % num_pics})
        util.photo.take_photos(num_pics)
    except:
        socketio.emit('failed', {"error": "FAILED :( - try again!"})
        socketio.emit('re-enable')
        return

    filenames = util.photo.get_filenames_of_recent_photos(num_pics, start_time)
    log.debug(filenames)

    socketio.emit('update_text', {"text": "Making %d thumbnails..." % len(filenames)})

    thumbnail_original_pairs = []

    # make thumbnails
    for current, filename in enumerate(filenames, 1):
        message = "Making thumbnail {current} of {total}".format(
            current=current,
            total=len(filenames)
        )
        socketio.emit('update_text', {"text": message})
        util.photo.make_thumbnail(filename)

        thumbnail_original_pairs = util.photo.get_thumbnail_original_pairs(
            originals=[filename]
        )
        log.debug(filename)
        # get the HTML for the recently-taken photo
        ctx = app.test_request_context()
        ctx.push()
        new_thumbnail_html = render_template(
            'photo_container.html',
            thumbnail_original_pairs=thumbnail_original_pairs,
            invisible=True
        )
        ctx.pop()
        socketio.emit('new_thumbnail', {"new_thumbnail_html": new_thumbnail_html})

    final_data = {
        "text": "TOOK %d PICTURES" % len(thumbnail_original_pairs)
    }
    socketio.emit('update_text', final_data)
    socketio.emit('re-enable')


if __name__ == '__main__':
    socketio_app.run(app)
