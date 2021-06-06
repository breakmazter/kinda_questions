FROM python:3.9.2

WORKDIR /create_link_product

COPY create_link_product_worker.py /create_link_product/create_link_product_worker.py
COPY settings.py /create_link_product/settings.py
COPY requirements.txt /create_link_product/requirements.txt
COPY actors_interface.py /create_link_product/actors_interface.py

COPY db/crud.py /create_link_product/db/crud.py
COPY db/models.py /create_link_product/db/models.py

RUN pip install --upgrade pip
RUN python -m pip install --no-cache-dir -U 'dramatiq[rabbitmq, redis]'==1.11.0
RUN python -m pip install --no-cache-dir -r requirements.txt

CMD ["dramatiq", "-t 4", "create_link_product_worker", "-Q", "josef_create_link_product_josef"]