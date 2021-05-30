import logging

import dramatiq
from dramatiq.results import Results
from dramatiq.results.backends import RedisBackend
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from settings import POSTGRES_URL_FIRST, POSTGRES_URL_SECOND, RABBITMQ_URL, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD
from actors_interface import create_youtube_channel, create_link, create_email, should_retry

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.crud import add_youtube_video, add_video
from db.models import YoutubeVideo, Video


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


def is_video(video_id, db_session):
    try:
        video = db_session.query(Video.id).filter(Video.id == video_id).first()

        if video:
            flag = True
        else:
            flag = False

        return flag
    except Exception as e:
        db_session.rollback()
        raise e


def is_youtube_video(youtube_video_id, db_session):
    try:
        youtube_video = db_session.query(YoutubeVideo.id).filter(YoutubeVideo.id == youtube_video_id).first()

        if youtube_video:
            flag = True
        else:
            flag = False

        return flag
    except Exception as e:
        db_session.rollback()
        raise e


@dramatiq.actor(queue_name='josef_create_youtube_video_josef',
                store_results=False, max_retries=3, time_limit=180000, retry_when=should_retry)
def create_youtube_video(youtube_video_id):
    session_insert = Session_insert()

    with Session_select() as session_select:

        youtube_video = session_insert.merge(session_select.query(YoutubeVideo).get(youtube_video_id))
        video = session_insert.merge(session_select.query(Video).get(youtube_video.external_id))

        if not is_video(video_id=youtube_video.external_id, db_session=session_insert):
            logging.info(f"Video with id={youtube_video.external_id} ---> exist!!!")
        else:
            add_video(video=video, db_session_insert=session_insert)
            logging.info(f"Video with id={youtube_video.external_id} ---> create!!!")

        if not is_youtube_video(youtube_video_id=youtube_video_id, db_session=session_insert):
            logging.info(f"YoutubeVideo with id={youtube_video_id} ---> exist!!!")
        else:
            add_youtube_video(video=youtube_video, db_session_insert=session_insert)
            logging.info(f"YoutubeVideo with id={youtube_video_id} ---> create!!!")

        create_link.send(video.id)
        create_youtube_channel.send(youtube_video.channel_id)
        create_email.send(youtube_video_id)

        session_insert.commit()
