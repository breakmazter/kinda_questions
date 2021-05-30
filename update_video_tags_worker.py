import dramatiq
from dramatiq.results import Results
from dramatiq.results.backends import RedisBackend
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from settings import POSTGRES_URL_FIRST, RABBITMQ_URL, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD
from actors_interface import should_retry

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.crud import update_youtube_video
from db.models import Product, Video, Link, YoutubeVideo

from utils.clean_text import clean_text
from utils.proccesing_text import top_words

broker = RabbitmqBroker(url=RABBITMQ_URL)
result_backend = RedisBackend(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
broker.add_middleware(Results(backend=result_backend))
dramatiq.set_broker(broker)

engine = create_engine(POSTGRES_URL_FIRST, pool_pre_ping=True,
                       pool_size=100, max_overflow=100, pool_recycle=3600)
Session = sessionmaker(bind=engine)


@dramatiq.actor(queue_name='josef_update_video_tags_josef',
                store_results=False, max_retries=3, time_limit=180000, retry_when=should_retry)
def update_video_tags(product_domain):
    session = Session()

    youtube_videos = session.query(YoutubeVideo.id, YoutubeVideo.description) \
        .join(Video, Video.id == YoutubeVideo.external_id) \
        .join(Video.links) \
        .join(Link.product) \
        .filter(Product.domain == product_domain).all()

    for ind, des in youtube_videos:
        update_youtube_video(video_id=ind,
                             video_data={'tags': top_words(5, clean_text(des))},
                             db_session_insert=session)
        print(f"YoutubeVideo with id={ind} update!!!")

    session.commit()
