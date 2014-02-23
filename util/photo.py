from stat import S_ISREG, ST_CTIME, ST_MODE
import os
import subprocess
import settings
from PIL import Image


def take_photos(num_photos):

    args = [
        'gphoto2',
        '--auto-detect',
        '--interval=1',
        '--frames={num_frames}'.format(num_frames=num_photos),
        '--capture-image-and-download',
        '--filename={originals_dir}/20%y-%m-%d_%H:%M:%S.%C'.format(
            originals_dir=settings.originals_dir
        )
    ]

    exit_code = subprocess.check_call(args)
    if exit_code != 0:
        raise Exception

def get_filenames_of_recent_photos(num_pics, since_timestamp):
    filenames = _get_recently_created_filenames(
        settings.originals_dir,
        limit=num_pics,
        since_timestamp=since_timestamp
     )
    return filenames

def make_thumbnail(path_to_file, shrink_factor=10):
    img = Image.open(path_to_file)
    new_size = [dimension / shrink_factor for dimension in img.size]
    img.thumbnail(new_size)
    filename = path_to_file.split('/')[-1]
    path = "{output_dir}/{filename}".format(
        output_dir=settings.thumbnails_dir,
        filename=filename
    )
    img.save(path)
    return path

def get_thumbnail_original_pairs(limit=30, since_timestamp=None):
    thumbnail_filenames = _get_recently_created_filenames(
        settings.thumbnails_dir,
        limit=limit,
        since_timestamp=since_timestamp
    )

    # trim off the 'static' dir
    thumbnail_filenames = [
        filename.replace(settings.static_dir, '.', 1)
        for filename in thumbnail_filenames
    ]

    thumbnail_original_pairs = [
        (thumbnail, thumbnail.replace(settings.thumbnails_dir_name, settings.originals_dir_name, 1))
        for thumbnail in thumbnail_filenames
    ]
    return thumbnail_original_pairs


def _get_recently_created_filenames(dirpath, limit=None, since_timestamp=None, extension='JPG'):
    # get all entries in the directory w/ stats
    entries = (
        os.path.join(dirpath, fn) for fn in os.listdir(dirpath)
        if fn.endswith(extension)
    )

    entries = ((os.stat(path), path) for path in entries)
    # leave only regular files, insert creation date
    entries = (
        (stat[ST_CTIME], path)
        for stat, path in entries if S_ISREG(stat[ST_MODE])
    )
    sorted_entries = sorted(entries, reverse=True)

    if since_timestamp:
        sorted_entries = filter(lambda x: x[0] > since_timestamp, sorted_entries)

    if limit:
        sorted_entries = sorted_entries[:limit]

    pathnames = [
        pathname for _, pathname in sorted_entries
    ]

    return pathnames

