FROM python:3

RUN pip install --no-cache-dir django mysqlclient django-graphos

WORKDIR /usr/src/app

COPY . .

WORKDIR /usr/src/app/groundstation

EXPOSE 8000/tcp

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]

