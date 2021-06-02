import logging

import dramatiq
from dramatiq.results import Results
from dramatiq.results.backends import RedisBackend
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from settings import POSTGRES_URL_FIRST, RABBITMQ_URL, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD
from actors_interface import should_retry

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import Video, YoutubeVideo

broker = RabbitmqBroker(url=RABBITMQ_URL)
result_backend = RedisBackend(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
broker.add_middleware(Results(backend=result_backend))
dramatiq.set_broker(broker)

engine = create_engine(POSTGRES_URL_FIRST, pool_pre_ping=True,
                       pool_size=100, max_overflow=100, pool_recycle=3600)
Session = sessionmaker(bind=engine)


@dramatiq.actor(queue_name='josef_delete_video_josef',
                store_results=True, max_retries=3, time_limit=180000, retry_when=should_retry)
def delete_video(video_id):

    with Session() as session:
        video = session.query(Video)\
            .join(YoutubeVideo, Video.id == YoutubeVideo.external_id)\
            .filter(YoutubeVideo.id == video_id).first()

        youtube_video = session.query(YoutubeVideo)\
            .filter(YoutubeVideo.id == video_id).first()

        session.delete(video)
        session.delete(youtube_video)

        session.commit()
        logging.info(f"Video with id={video_id} delete!!!")
