FROM python:3.7-slim


RUN apt-get clean \
    && apt-get -y update
RUN apt-get -y install nginx \
    && apt-get -y install python3-dev \
    && apt-get -y install build-essential

COPY requirements.txt /srv/flask_app/
WORKDIR /srv/flask_app

RUN pip install -r requirements.txt --src /usr/local/src

COPY . /srv/flask_app


COPY nginx.conf /etc/nginx
RUN chmod +x ./start.sh
CMD ["./start.sh"]