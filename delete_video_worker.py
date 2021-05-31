import dramatiq
from dramatiq.results import Results
from dramatiq.results.backends import RedisBackend
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from settings import POSTGRES_URL_FIRST, RABBITMQ_URL, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD
from actors_interface import should_retry

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import Product, Video, Link, YoutubeVideo

broker = RabbitmqBroker(url=RABBITMQ_URL)
result_backend = RedisBackend(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
broker.add_middleware(Results(backend=result_backend))
dramatiq.set_broker(broker)

engine = create_engine(POSTGRES_URL_FIRST, pool_pre_ping=True,
                       pool_size=100, max_overflow=100, pool_recycle=3600)
Session = sessionmaker(bind=engine)


def is_product(video_id, db_session):
    try:
        product = db_session.query(Product.domain)\
            .join(Product.links)\
            .join(Link.videos)\
            .filter(Video.id == video_id).first()

        if product:
            flag = True
        else:
            flag = False

        return flag
    except Exception as e:
        db_session.rollback()
        raise e


@dramatiq.actor(queue_name='josef_delete_video_josef',
                store_results=False, max_retries=3, time_limit=180000, retry_when=should_retry)
def delete_video(video_id):
    session = Session()

    if not is_product(video_id=video_id, db_session=session):
        session.query(Video)\
            .join(YoutubeVideo, Video.id == YoutubeVideo.external_id)\
            .filter(YoutubeVideo.id == video_id).delete()

        session.commit()
        print(f"Video with id={video_id} delete!!!")
