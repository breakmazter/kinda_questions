import dramatiq
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from actors_interface import create_youtube_video, create_email, delete_video
from db.models import YoutubeVideo, YoutubeChannel


##########################
# CONFIGS FOR POSTGRESQL #
##########################

POSTGRES_HOST = '127.0.0.1'
POSTGRES_PORT = 5432
POSTGRESS_DB = 'oxicore-video-products'
POSTGRES_LOGIN = 'postgres'
POSTGRES_PASSWORD = 'zPc0HxpCfHxpNu0D'
POSTGRES_URL = f'postgresql://{POSTGRES_LOGIN}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRESS_DB}'

engine = create_engine(POSTGRES_URL, pool_pre_ping=True,
                       pool_size=100, max_overflow=100, pool_recycle=3600)
Session = sessionmaker(bind=engine)


def split(arr, size):
    mass = []
    while len(arr) > size:
        pic = arr[:size]
        mass.append(pic)
        arr = arr[size:]
    mass.append(arr)
    return mass


def get_youtube_video_id(batch_size: int):

    with Session() as session:
        video_ids = session.query(YoutubeVideo.id).filter(YoutubeVideo.description_lang == 'ru').limit(100000).all()

        for video_id in split(video_ids, batch_size):
            print("Hi")
            dramatiq.group([create_youtube_video.message(ind.id) for ind in video_id]).run()


def get_youtube_channel_id(batch_size: int):
    with Session() as session:
        channel_ids = session.query(YoutubeChannel.id).limit(100000).all()

        for channel_id in split(channel_ids, batch_size):
            dramatiq.group([create_email.message(ind.id) for ind in channel_id]).run()


if __name__ == '__main__':
    get_youtube_video_id(10)
