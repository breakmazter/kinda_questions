import logging

import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from dramatiq.results import Results
from dramatiq.results.backends import RedisBackend
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from actors_interface import should_retry
from db.crud import update_youtube_video
from db.models import YoutubeVideo
from settings import POSTGRES_URL_SON, RABBITMQ_URL, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD
from utils.clean_text import clean_text
from utils.proccesing_text import top_words

broker = RabbitmqBroker(url=RABBITMQ_URL)
result_backend = RedisBackend(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
broker.add_middleware(Results(backend=result_backend))
dramatiq.set_broker(broker)

engine = create_engine(POSTGRES_URL_SON, pool_pre_ping=True,
                       pool_size=100, max_overflow=100, pool_recycle=3600)
Session = sessionmaker(bind=engine)


@dramatiq.actor(queue_name='josef_update_video_tags_josef',
                store_results=True, max_retries=3, time_limit=180000, retry_when=should_retry)
def update_video_tags(youtube_video_id):
    with Session() as session:
        youtube_videos = session.query(YoutubeVideo.id, YoutubeVideo.description) \
            .filter(YoutubeVideo.id == youtube_video_id).first()

        update_youtube_video(video_id=youtube_videos.id,
                             video_data={'tags': top_words(5, clean_text(youtube_videos.description))},
                             db_session_insert=session)

        logging.info(f"YoutubeVideo with id={youtube_videos.id} ---> update!!!")

        session.commit()
