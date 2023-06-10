FROM ubuntu:20.04

ENV PYTHONUNBUFFERED=1

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install python3.8 python3-pip

# psycopg2
RUN apt-get -y install libpq-dev
RUN pip3 install psycopg2

# mkdir
RUN mkdir /var/log/django/
RUN chown www-data /var/log/django/

# install git
RUN apt-get -y install git

# install requirements
COPY ./requirements.txt /docker/
WORKDIR /docker
RUN pip3 install -r requirements.txt
RUN rm -r /docker

# workdir
WORKDIR /webapps
