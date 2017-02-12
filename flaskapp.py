from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask import url_for
import flask_socketio as socketio
from flask_socketio import SocketIO

import util.sass
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


@socketio_app.on('take_pics')
def ws_take_pics(message):
    num_pics = int(message['num_pics'])

    assert num_pics in settings.framenum_values
    successful_pics = 0

    for index in range(1, num_pics + 1):
        message = "Taking {index} of {total} pics".format(index=index, total=num_pics)
        socketio.emit('update_text', {"text": message})
        try:
            filename = util.photo.take_photo()
            successful_pics += 1
        except Exception as e:
            message = "FAILED on {index} of {total}".format(index=index, total=num_pics)
            socketio.emit('failed', {"error": message})
            continue

        try:
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
        except Exception as e:
            socketio.emit('failed', {"error": "Error making thumbnail"})

    final_data = {
        "text": "TOOK {successes} PICTURES".format(successes=successful_pics)
    }
    socketio.emit('update_text', final_data)
    socketio.emit('re-enable')


if __name__ == '__main__':
    socketio_app.run(app)
