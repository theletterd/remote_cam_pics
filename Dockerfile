FROM armv7/armhf-ubuntu_core:latest

RUN apt-get update
RUN apt-get install -y python3.5 python3-pip python3-setuptools \
  -o APT::Install-Recommends=true \
  -o APT::Install-Suggests=false

RUN ln -s /usr/bin/python3.5 /usr/bin/python
RUN ln -s /usr/bin/pip3 /usr/bin/pip

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install setuptools
RUN pip install -r requirements.txt

EXPOSE 8000
CMD gunicorn -k gevent --workers=5 --log-level=debug -b 0.0.0.0:8000 flaskapp:app