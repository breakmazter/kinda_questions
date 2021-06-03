FROM python:3.9.2

WORKDIR /update_product_description

COPY update_product_description_worker.py /create_email/update_product_description_worker.py
COPY settings.py /update_product_description/settings.py
COPY requirements.txt /update_product_description/requirements.txt
COPY actors_interface.py /update_product_description/actors_interface.py

COPY db/crud.py /update_product_description/db/crud.py
COPY db/models.py /update_product_description/db/models.py

COPY utils/clean_text.py /update_product_description/utils/clean_text.py

RUN pip install --upgrade pip
RUN python -m pip install --no-cache-dir -U 'dramatiq[rabbitmq, redis]'==1.11.0
RUN python -m pip install --no-cache-dir -r requirements.txt

CMD ["dramatiq", "-p 8", "-t 16", "update_product_description_worker", "-Q", "josef_update_product_description_josef"]
