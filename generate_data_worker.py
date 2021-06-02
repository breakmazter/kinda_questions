import dramatiq

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import POSTGRES_URL_SECOND
from actors_interface import create_youtube_video

from db.models import YoutubeVideo


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


def get_ids(count: int, batch_size: int):
    with Session() as session:
        video_ids = session.query(YoutubeVideo.id).filter(YoutubeVideo.description_lang == 'ru').limit(count).all()

        for video_id in split(video_ids, batch_size):
            dramatiq.group([create_youtube_video.message(ind.id) for ind in video_id]).run()


if __name__ == '__main__':
    get_ids(100000, 1000)
