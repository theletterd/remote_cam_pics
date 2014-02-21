from stat import S_ISREG, ST_CTIME, ST_MODE
import os
import usb


def get_recently_created_filenames(dirpath, limit=None, extension='jpg'):
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
    

def reset_usb(camera_manufacturer):
    all_usb_devices = usb.core.find(find_all=True)

    for device in all_usb_devices:
        try:
            device_product = usb.util.get_string(device, 256, device.iProduct)
            if camera_manufacturer.lower() in device_product.lower():
                device.reset()
                return
        except:
            pass
