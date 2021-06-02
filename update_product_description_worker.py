import logging

import dramatiq
from dramatiq.results import Results
from dramatiq.results.backends import RedisBackend
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from settings import POSTGRES_URL_FIRST, RABBITMQ_URL, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD
from actors_interface import should_retry

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.crud import update_product

from utils.clean_text import clean_text

broker = RabbitmqBroker(url=RABBITMQ_URL)
result_backend = RedisBackend(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
broker.add_middleware(Results(backend=result_backend))
dramatiq.set_broker(broker)


engine_insert = create_engine(POSTGRES_URL_FIRST, pool_pre_ping=True,
                              pool_size=100, max_overflow=100, pool_recycle=3600)
Session_insert = sessionmaker(bind=engine_insert)


@dramatiq.actor(queue_name='josef_update_product_description_josef',
                store_results=True, max_retries=3, time_limit=180000, retry_when=should_retry)
def update_product_description(product_domain, product_description):
    clean_product_data = {'description': clean_text(product_description)}

    with Session_insert() as session_insert:
        update_product(product_domain=product_domain, product_data=clean_product_data, db_session_insert=session_insert)
        session_insert.commit()

        logging.info(f"Product with id={product_domain} ---> update!!!")
