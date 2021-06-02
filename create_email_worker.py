import logging

import dramatiq
from dramatiq.results import Results
from dramatiq.results.backends import RedisBackend
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from settings import POSTGRES_URL_FIRST, RABBITMQ_URL, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD
from actors_interface import should_retry

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import YoutubeVideo, YoutubeChannel, Email
from db.crud import add_email

broker = RabbitmqBroker(url=RABBITMQ_URL)
result_backend = RedisBackend(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
broker.add_middleware(Results(backend=result_backend))
dramatiq.set_broker(broker)

engine = create_engine(POSTGRES_URL_FIRST, pool_pre_ping=True,
                       pool_size=100, max_overflow=100, pool_recycle=3600)
Session = sessionmaker(bind=engine)


@dramatiq.actor(queue_name='josef_create_email_josef',
                store_results=True, max_retries=3, time_limit=180000, retry_when=should_retry)
def create_email(channel_id):
    with Session() as session:
        videos_description = session.query(YoutubeVideo.description, YoutubeChannel.description) \
            .join(YoutubeChannel, YoutubeChannel.id == YoutubeVideo.channel_id) \
            .filter(YoutubeChannel.id == channel_id).all()

        for video in videos_description:
            email_data = {'channel_id': channel_id,
                          'channel_description': video[1],
                          'video_description': video[0]}

            email = Email(**email_data)

        add_email(email=session.merge(email), db_session_insert=session)
        logging.info(f"Email with channel_id={channel_id} ---> create!!!")

        session.commit()
