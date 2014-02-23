remote_cam_pics
==============

My usage
--------
* Have a phone where you can create a portable wifi-hotspot
* Install `remote-cam-pics` onto a raspberrypi and run
* Have raspberrypi connect to your phone wifi
* Connect DSLR to raspberrypi
* Visit URL of app using your phone
* **pose!**
* Click a button

Prerequisites:
-------------
  * gphoto2
  * python-dev (needed for building Pillow)

Installation:
-------------
* `$ virtualenv env`
* `$ source env/bin/activate`
* `$ pip install -r requirements.txt`

To run:
-------
* `$ gunicorn -k flask_sockets.worker --workers=5 -b 0.0.0.0:8000 flaskapp:app`

Notes:
------
See settings.py for various, uh, settings.

I'm using `supervisor` to manage gunicorn so that the webapp will run whenever the raspberrypi is running, a good tutorial of which is \ [http://www.onurguzel.com/managing-gunicorn-processes-with-supervisor/](http://www.onurguzel.com/managing-gunicorn-processes-with-supervisor/)

  * **pyusb** is being used to reset the usb-connection between the DSLR and the raspberrypi. (was originally doing this - [http://marc.info/?l=linux-usb&m=121459435621262&w=2](http://marc.info/?l=linux-usb&m=121459435621262&w=2)
  * **pyscss** is being used for Sass sexiness.
  * **Pillow** for the image-resizing. This could probably be done better and in a less heavy-weight fashion.
  * **flask-sockets** greatly simplified the usage of web-sockets
