import logging

import dramatiq
from dramatiq.results import Results
from dramatiq.results.backends import RedisBackend
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from settings import POSTGRES_URL_FIRST, POSTGRES_URL_SECOND, RABBITMQ_URL, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD
from actors_interface import should_retry, update_product_description, create_link

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.crud import add_product
from db.models import Link, Product, Video

broker = RabbitmqBroker(url=RABBITMQ_URL)
result_backend = RedisBackend(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
broker.add_middleware(Results(backend=result_backend))
dramatiq.set_broker(broker)

engine_select = create_engine(POSTGRES_URL_SECOND, pool_pre_ping=True,
                              pool_size=100, max_overflow=100, pool_recycle=3600)
Session_select = sessionmaker(bind=engine_select)

engine_insert = create_engine(POSTGRES_URL_FIRST, pool_pre_ping=True,
                              pool_size=100, max_overflow=100, pool_recycle=3600)
Session_insert = sessionmaker(bind=engine_insert)


def is_product(product_id, db_session):
    try:
        product = db_session.query(Product.domain).filter(Product.domain == product_id).first()

        if product:
            flag = True
        else:
            flag = False

        return flag
    except Exception as e:
        db_session.rollback()
        raise e


@dramatiq.actor(queue_name='josef_create_product_josef',
                store_results=False, max_retries=3, time_limit=180000, retry_when=should_retry)
def create_product(video_id):
    session_insert = Session_insert()

    with Session_select() as session_select:
        products = session_select.query(Product).join(Product.links, Link.videos).filter(Video.id == video_id).all()

        for product in products:
            if is_product(product_id=product.domain, db_session=session_insert):
                logging.info(f"Product with id={product.domain} ---> exist!!!")
            else:
                add_product(session_insert.merge(product), db_session_insert=session_insert)
                logging.info(f"Product with id={product.domain} ---> create!!!")

                update_product_description.send(product.domain, product.description)
                create_link.send(video_id)

        session_insert.commit()


create_product("7RjJEGLeBBk")