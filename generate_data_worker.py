import dramatiq
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from actors_interface import create_youtube_video
from db.models import YoutubeVideo

# CONFIGS FOR POSTGRESQL_SECOND

POSTGRES_HOST_SECOND = '127.0.0.1'
POSTGRES_PORT_SECOND = 5434
POSTGRESS_DB_SECOND = 'oxicore-video-products'
POSTGRES_LOGIN_SECOND = 'postgres'
POSTGRES_PASSWORD_SECOND = 'zPc0HxpCfHxpNu0D'

POSTGRES_URL_SECOND = f'postgresql://{POSTGRES_LOGIN_SECOND}:' \
                      f'{POSTGRES_PASSWORD_SECOND}@{POSTGRES_HOST_SECOND}:' \
                      f'{POSTGRES_PORT_SECOND}/{POSTGRESS_DB_SECOND}'

engine = create_engine(POSTGRES_URL_SECOND, pool_pre_ping=True,
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


def get_ids(batch_size: int):
    with Session() as session:
        video_ids = session.query(YoutubeVideo.id).filter(YoutubeVideo.description_lang == 'ru').all()

        for video_id in split(video_ids, batch_size):
            dramatiq.group([create_youtube_video.message(ind.id) for ind in video_id]).run()


if __name__ == '__main__':
    get_ids(1000)
