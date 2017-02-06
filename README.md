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
* `$ docker build -t remote_cam_pics .`


To run:
-------
* `$ docker run -p 8000:8000 --privileged -v /dev/bus/usb:/dev/bus/usb remote_cam_pics`

Notes:
------
See settings.py for various, uh, settings.
