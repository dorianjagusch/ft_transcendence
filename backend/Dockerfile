FROM python:3.10.12

RUN mkdir app

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y netcat-openbsd gcc openssl && \
    apt-get clean

RUN apt-get install libpq-dev
COPY requirements.txt app/
COPY ssl_setup.sh app/
COPY entrypoint.sh app/

WORKDIR /app

RUN pip install --upgrade pip \
	&& pip install -r requirements.txt \
    &&  sh ssl_setup.sh \
	&& chmod 755 entrypoint.sh

EXPOSE 8080
