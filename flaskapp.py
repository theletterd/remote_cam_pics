from flask import Flask
from flask import render_template
from flask_sockets import Sockets

import json
import util.sass
import util.photo
import settings

import logging


app = Flask(__name__)
sockets = Sockets(app)

log = logging.getLogger(__file__)
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(msg)s")

def send_message(ws, message):
    ws.send(json.dumps({"text": message}))

def send_error(ws, message):
    ws.send(json.dumps({"error": message}))

def send_thumbnail_html(ws, html):
    ws.send(json.dumps({"new_thumbnail_html": html}))


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

@app.route('/all', methods=['GET'])
def all_images():
    # make this a deploy script or something
    if app.debug:
        util.sass.regenerate_scss()

    thumbnail_original_pairs = util.photo.get_thumbnail_original_pairs(limit=1000)

    return render_template(
        'index.html',
        thumbnail_original_pairs=thumbnail_original_pairs,
        framenum_values=settings.framenum_values,
    )


@sockets.route('/take_pics')
def ws_take_pics(ws):
    payload = json.loads(ws.receive())
    num_pics = int(payload['num_pics'])

    assert num_pics in settings.framenum_values
    successful_pics = 0
    successful_thumbs = 0

    for index in range(1, num_pics + 1):
        send_message(ws, "Taking {index} of {total} pics".format(index=index, total=num_pics))
        try:
            filename = util.photo.take_photo()
            log.info(filename)
            successful_pics += 1
        except Exception as e:
            send_error(ws, "FAILED on {index} of {total}".format(index=index, total=num_pics))
            log.info(e)
            continue

        try:
            util.photo.make_thumbnail(filename)
            thumbnail_original_pairs = util.photo.get_thumbnail_original_pairs(
                originals=[filename]
            )
            log.debug(filename)
            log.info(thumbnail_original_pairs)
            # get the HTML for the recently-taken photo
            ctx = app.test_request_context()
            ctx.push()
            new_thumbnail_html = render_template(
                'photo_container.html',
                thumbnail_original_pairs=thumbnail_original_pairs,
                invisible=True
            )
            ctx.pop()
            send_thumbnail_html(ws, new_thumbnail_html)
            successful_thumbs += 1
        except Exception as e:
            send_error(ws, "Error making thumbnail")
            log.info(e)

    send_message(
        ws,
        "TOOK {successes}/{attempts} PICTURES - GENERATED {thumbs} THUMBNAILS".format(
            successes=successful_pics,
            attempts=num_pics,
            thumbs=successful_thumbs
        )
    )
