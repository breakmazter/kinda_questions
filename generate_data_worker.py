import dramatiq
from dramatiq.results import Results
from dramatiq.results.backends import RedisBackend
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from settings import REDIS_PORT, REDIS_HOST, REDIS_PASSWORD, RABBITMQ_URL, POSTGRES_URL_SECOND
from actors_interface import create_youtube_video

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from db.models import YoutubeVideo

engine = create_engine(POSTGRES_URL_SECOND, pool_size=20, max_overflow=20, poolclass=QueuePool)
Session = sessionmaker(bind=engine)

broker = RabbitmqBroker(url=RABBITMQ_URL)
result_backend = RedisBackend(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
broker.add_middleware(Results(backend=result_backend))
dramatiq.set_broker(broker)


def get_ids():
    with Session() as session:
        video_ids = session.query(YoutubeVideo.id).filter(YoutubeVideo.description_lang == 'ru').limit(100).all()
        for video_id in video_ids:
            create_youtube_video.send(video_id.id)
            print(f"{video_id.id} - yes")


if __name__ == '__main__':
    get_ids()

# TODO create normal worker relations !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
