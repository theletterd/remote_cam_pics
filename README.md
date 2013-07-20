remote_cam_pics
===============

Bash script which uses gphoto2 and ufraw-batch to trigger a DSLR to take pictures,
and generate an HTML index page to view them.


I've been using this as follows:

#1 - connect laptop to camera over USB
#2 - share folder locally using "python -m SimpleHTTPServer"
#3 - ssh into laptop from phone
#4 - POSE
#5 - run script on laptop from phone
#6 - load up page on phone to see newly taken photos.