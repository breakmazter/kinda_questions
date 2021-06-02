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


def split(arr, size):
    mass = []
    while len(arr) > size:
        pic = arr[:size]
        mass.append(pic)
        arr = arr[size:]
    mass.append(arr)
    return mass


def get_ids(count, batch_size):
    with Session() as session:
        video_ids = session.query(YoutubeVideo.id).filter(YoutubeVideo.description_lang == 'ru').limit(count).all()

        for video_id in split(video_ids, batch_size):
            dramatiq.group([create_youtube_video.message(ind.id) for ind in video_id]).run()


if __name__ == '__main__':
    get_ids(100000, 1000)
