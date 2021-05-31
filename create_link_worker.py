import logging

import dramatiq
from dramatiq.results import Results
from dramatiq.results.backends import RedisBackend
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from settings import POSTGRES_URL_FIRST, POSTGRES_URL_SECOND, RABBITMQ_URL, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD
from actors_interface import should_retry

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.crud import add_link, add_videolink
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


def is_link(link_id, db_session):
    try:
        link = db_session.query(Link.link).filter(Link.link == link_id).first()

        if link:
            flag = True
        else:
            flag = False

        return flag
    except Exception as e:
        db_session.rollback()
        raise e


@dramatiq.actor(queue_name='josef_create_link_josef',
                store_results=False, max_retries=3, time_limit=180000, retry_when=should_retry)
def create_link(video_id):
    session_insert = Session_insert()

    with Session_select() as session_select:
        links = session_select.query(Link)\
                .join(VideoLink, VideoLink.c.link_id == Link.link)\
                .filter(VideoLink.c.video_id == video_id).all()

        for link in links:
            if is_link(link_id=link.link, db_session=session_insert):
                logging.info(f"Link with id={link.link} ---> exist!!!")
            else:
                add_link(session_insert.merge(link), db_session_insert=session_insert)
                add_videolink(video_id=video_id, link_id=link.link, db_session_insert=session_insert)
                logging.info(f"Link with id={link.link} ---> create!!!")

        session_insert.commit()
