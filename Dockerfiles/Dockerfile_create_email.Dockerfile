FROM python:3.9.2-slim-buster

WORKDIR /create_email

COPY ../create_email_worker.py /create_email/create_email_worker.py
COPY ../settings.py /create_email/settings.py
COPY ../requirements/create_email_requirements.txt /create_email/create_email_requirements.txt
COPY ../actors_interface.py /create_email/actors_interface.py

COPY ../db/crud.py /create_email/db/crud.py
COPY ../db/models.py /create_email/db/models.py

RUN pip install --upgrade pip
RUN python -m pip install --no-cache-dir -U 'dramatiq[rabbitmq, redis]'==1.11.0
RUN python -m pip install -r create_email_requirements.txt
RUN python -m pip install psycopg2-binary==2.8.6

CMD ["dramatiq", "-p 8", "-t 8", "create_email_worker", "-Q", "josef_create_email_josef"]