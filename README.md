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
  * docker


To build:
---------
* `$ make build_image`


To run:
-------
* `$ make start_container`

To stop:
--------
* `$ make stop_container`

To remove container:
--------------------
* `$ make clean`


Notes:
------
Original images are stored in `static/originals`.
See settings.py for various, uh, settings.
