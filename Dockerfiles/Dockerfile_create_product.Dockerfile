FROM python:3.9.2-slim-buster

WORKDIR /create_product

COPY ../create_product_worker.py /create_product/create_product_worker.py
COPY ../settings.py /create_product/settings.py
COPY ../requirements/create_product_requirements.txt /create_product/create_product_requirements.txt
COPY ../actors_interface.py /create_product/actors_interface.py

COPY ../db/crud.py /create_product/db/crud.py
COPY ../db/models.py /create_product/db/models.py

RUN pip install --upgrade pip
RUN python -m pip install --no-cache-dir -U 'dramatiq[rabbitmq, redis]'==1.11.0
RUN python -m pip install -r create_product_requirements.txt
RUN python -m pip install psycopg2-binary==2.8.6

CMD ["dramatiq", "-p 8", "-t 8", "create_product_worker", "-Q", "josef_create_product_josef"]