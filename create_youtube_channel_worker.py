import logging

import dramatiq
from dramatiq.results import Results
from dramatiq.results.backends import RedisBackend
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from settings import POSTGRES_URL_FIRST, POSTGRES_URL_SECOND, RABBITMQ_URL, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD
from actors_interface import should_retry, create_email

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from db.crud import add_youtube_channel
from db.models import YoutubeChannel

broker = RabbitmqBroker(url=RABBITMQ_URL)
result_backend = RedisBackend(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
broker.add_middleware(Results(backend=result_backend))
dramatiq.set_broker(broker)

engine_select = create_engine(POSTGRES_URL_SECOND, pool_size=20, max_overflow=20, poolclass=QueuePool)
Session_select = sessionmaker(bind=engine_select)

engine_insert = create_engine(POSTGRES_URL_FIRST, pool_size=20, max_overflow=20, poolclass=QueuePool)
Session_insert = sessionmaker(bind=engine_insert)


def is_youtube_channel(youtube_channel_id, db_session):
    try:
        youtube_channel = db_session.query(YoutubeChannel.id).filter(YoutubeChannel.id == youtube_channel_id).scalar()

        if youtube_channel:
            flag = True
        else:
            flag = False

        return flag
    except Exception as e:
        db_session.rollback()
        raise e


@dramatiq.actor(queue_name='josef_create_youtube_channel_josef',
                store_results=True, max_retries=3, time_limit=180000, retry_when=should_retry)
def create_youtube_channel(channel_id):

    with Session_select() as session_select, Session_insert() as session_insert:
        channel = session_select.query(YoutubeChannel).get(channel_id)

        if is_youtube_channel(youtube_channel_id=channel_id, db_session=session_insert):
            logging.info(f"YoutubeChannel with id={channel_id} ---> exist!!!")
        else:
            add_youtube_channel(channel=session_insert.merge(channel), db_session_insert=session_insert)
            logging.info(f"YoutubeChannel with id={channel_id} ---> create!!!")

            create_email.send(channel_id)

        session_insert.commit()
