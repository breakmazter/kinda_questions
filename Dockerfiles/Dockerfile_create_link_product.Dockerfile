FROM python:3.9.2-slim-buster

WORKDIR /create_link

COPY ../create_link_product_worker.py /create_link/create_link_worker.py
COPY ../settings.py /create_link/settings.py
COPY ../requirements/create_link_product_requirements.txt /create_link/create_link_requirements.txt
COPY ../actors_interface.py /create_link/actors_interface.py

COPY ../db/crud.py /create_link/db/crud.py
COPY ../db/models.py /create_link/db/models.py

RUN pip install --upgrade pip
RUN python -m pip install --no-cache-dir -U 'dramatiq[rabbitmq, redis]'==1.11.0
RUN python -m pip install -r create_link_requirements.txt
RUN python -m pip install psycopg2-binary==2.8.6

CMD ["dramatiq", "-p 8", "-t 8", "create_link_worker", "-Q", "josef_create_link_josef"]