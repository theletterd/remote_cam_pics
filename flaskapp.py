from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from stat import S_ISREG, ST_CTIME, ST_MODE
import os

app = Flask(__name__)

FRAMENUM_VALUES = [1, 5, 10, 20]

def get_most_recent_thumbnails(limit=30):
    dirpath = 'static/thumbs'
    # get all entries in the directory w/ stats
    entries = (
        os.path.join(dirpath, fn) for fn in os.listdir(dirpath)
        if fn.endswith('.jpg')
    )
    entries = ((os.stat(path), path) for path in entries)
    # leave only regular files, insert creation date
    entries = (
        (stat[ST_CTIME], path)
        for stat, path in entries if S_ISREG(stat[ST_MODE])
    )
    sorted_entries = sorted(entries)[:limit]
    pathnames = [
        pathname.replace('static/', '', 1)
        for _, pathname in sorted_entries
    ]

    return pathnames

@app.route('/', methods=['GET'])
def index():
    thumbnails = get_most_recent_thumbnails()
    return render_template(
        'index.html',
        thumbnails=thumbnails,
        framenum_values=FRAMENUM_VALUES
    )

@app.route('/take_pics', methods=['POST'])
def take_pics():
    pics_to_take = int(request.form['framenum'])
    print pics_to_take
    assert pics_to_take in FRAMENUM_VALUES

    os.system('util/take_ten_pics ./static/originals/ ./static/thumbs/ %d' % pics_to_take)
    # ok this is where we do the business as it were.
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
