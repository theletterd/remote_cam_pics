from stat import S_ISREG, ST_CTIME, ST_MODE
import os
import settings
import gphoto2 as gp
from PIL import Image
import datetime


def take_photo():
    context = gp.Context()
    camera = gp.Camera()
    camera.init(context)

    file_path = gp.check_result(
        gp.gp_camera_capture(
            camera,
            gp.GP_CAPTURE_IMAGE,
            context
        )
    )

    # TODO - label the photos by date - YYYY-MM-DD-HH-MM-SS or something.
    datestr = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f ')
    target = os.path.join(settings.originals_dir, datestr + file_path.name)
    camera_file = gp.check_result(
        gp.gp_camera_file_get(
            camera,
            file_path.folder,
            file_path.name,
            gp.GP_FILE_TYPE_NORMAL, context
        )
    )
    gp.check_result(
        gp.gp_file_save(
            camera_file,
            target
        )
    )
    gp.check_result(
        gp.gp_camera_file_delete(
            camera,
            file_path.folder,
            file_path.name,
            context
        )
    )
    gp.gp_camera_exit(camera, context)

    return target


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


def get_thumbnail_original_pairs(limit=30, originals=None):
    if originals:
        thumbnail_filenames = [
            original.replace(settings.originals_dir_name, settings.thumbnails_dir_name, 1)
            for original in originals
        ]
    else:
        thumbnail_filenames = _get_recently_created_filenames(
            settings.thumbnails_dir,
            limit=limit,
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


def _get_recently_created_filenames(dirpath, limit=None, extension='JPG'):
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

    if limit:
        sorted_entries = sorted_entries[:limit]

    pathnames = [
        pathname for _, pathname in sorted_entries
    ]

    return pathnames
