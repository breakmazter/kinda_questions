import logging

import dramatiq
from dramatiq.results import Results
from dramatiq.results.backends import RedisBackend
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import POSTGRES_URL_FIRST, POSTGRES_URL_SECOND, RABBITMQ_URL, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD
from actors_interface import should_retry, update_product_description

from db.crud import add_link, add_videolink, add_product, is_link, is_product
from db.models import VideoLink, Link


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


@dramatiq.actor(queue_name='josef_create_link_product_josef',
                store_results=True, max_retries=3, time_limit=180000, retry_when=should_retry)
def create_link_product(video_id):
    with Session_select() as session_select, Session_insert() as session_insert:
        links = session_select.query(Link) \
            .join(VideoLink, VideoLink.c.link_id == Link.link) \
            .filter(VideoLink.c.video_id == video_id).all()

        for link in links:

            if is_link(link_id=link.link, db_session=session_insert):
                logging.info(f"Link with id={link.link} ---> exist!!!")
            else:
                if not is_product(product_id=link.product_domain, db_session=session_insert):
                    add_product(product=session_insert.merge(link.product), db_session_insert=session_insert)
                    update_product_description.send(link.product.domain, link.product.description)

                add_link(session_insert.merge(link), db_session_insert=session_insert)
                add_videolink(video_id=video_id, link_id=link.link, db_session_insert=session_insert)

                session_insert.commit()
                logging.info(f"Link with id={link.link} ---> create!!!")


if __name__ == "__main__":
    create_link_product("vTc6vYLnf2A")