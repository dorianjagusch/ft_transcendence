FROM python:3.10.12

RUN mkdir app

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y netcat-openbsd gcc && \
    apt-get clean

RUN apt-get install libpq-dev
# postgresql
COPY requirements.txt app/
COPY . app/

WORKDIR /app

RUN pip install --upgrade pip \
	&& pip install -r requirements.txt

EXPOSE 8080

CMD bash -c "sleep 10 && \
	python manage.py makemigrations && \
	python manage.py migrate && \
	python manage.py runserver 0.0.0.0:8080"
