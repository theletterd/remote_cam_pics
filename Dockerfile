FROM armv7/armhf-ubuntu_core:latest

RUN apt-get update
RUN apt-get install -y \
  gcc \
  gphoto2 \
  libgphoto2-dev \
  libjpeg-dev \
  pkg-config \
  python3-dev \
  python3-pip \
  python3-setuptools \
  python3-wheel \
  python3.5 \
  -o APT::Install-Recommends=false \
  -o APT::Install-Suggests=false

# Pillow is broken. after 3.0.0, requires zlib and jpeg libs
# see http://pillow.readthedocs.io/en/3.1.x/installation.html

RUN ln -s /usr/bin/python3.5 /usr/bin/python
RUN ln -s /usr/bin/pip3 /usr/bin/pip

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8000
CMD gunicorn -k flask_sockets.worker --workers=5 --log-level=debug -b 0.0.0.0:8000 flaskapp:app