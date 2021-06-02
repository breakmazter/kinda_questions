import logging

import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from dramatiq.results import Results
from dramatiq.results.backends import RedisBackend
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from actors_interface import create_youtube_channel, create_link_product, update_video_tags, should_retry, delete_video
from db.crud import add_object, is_video, is_youtube_video
from db.models import YoutubeVideo, Video, Product, Link
from settings import POSTGRES_URL_FIRST, POSTGRES_URL_SECOND, RABBITMQ_URL, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD

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


@dramatiq.actor(queue_name='josef_create_youtube_video_josef',
                store_results=True, max_retries=3, time_limit=180000, retry_when=should_retry)
def create_youtube_video(youtube_video_id):
    session_insert = Session_insert()

    with Session_select() as session_select:
        youtube_video = session_select.query(YoutubeVideo).get(youtube_video_id)
        video = session_select.query(Video).get(youtube_video.external_id)

        video_product = session_select.query(Product.domain)\
            .join(Product.links, Link.videos)\
            .filter(Video.id == video.id).first()

        if not is_video(video_id=youtube_video.external_id, db_session=session_insert) \
                and not is_youtube_video(youtube_video_id=youtube_video_id, db_session=session_insert):

            add_object(obj=session_insert.merge(video), db_session_insert=session_insert)
            logging.info(f"Video with id={youtube_video.external_id} ---> create!!!")

            add_object(obj=session_insert.merge(youtube_video), db_session_insert=session_insert)
            logging.info(f"YoutubeVideo with id={youtube_video_id} ---> create!!!")

            if video_product:
                update_video_tags.send(youtube_video_id)
                create_youtube_channel.send(youtube_video.channel_id)
                create_link_product.send(video.id)
            else:
                delete_video.send(youtube_video_id)

        else:
            logging.info(f"Video with id={youtube_video.external_id} ---> exist!!!")
            logging.info(f"YoutubeVideo with id={youtube_video_id} ---> exist!!!")

        session_insert.commit()
