FROM python:3.10.12

RUN mkdir app

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y netcat-openbsd gcc && \
    apt-get clean

COPY requirements.txt app/
COPY . app/

WORKDIR /app

RUN pip install --upgrade pip \
	&& pip install -r requirements.txt

RUN python manage.py makemigrations && \
	python manage.py migrate

EXPOSE 8001

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
