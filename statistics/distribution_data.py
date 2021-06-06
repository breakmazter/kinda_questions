import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine, distinct
from sqlalchemy.orm import sessionmaker

from db.models import *

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


def count_objects():
    with Session() as session:
        count_video = session.query(YoutubeVideo.id).filter(YoutubeVideo.description_lang == 'ru').count()

        count_channel = session.query(distinct(YoutubeChannel.id))\
            .join(YoutubeVideo, YoutubeChannel.id == YoutubeVideo.channel_id)\
            .filter(YoutubeVideo.description_lang == 'ru').count()

        count_link = session.query(distinct(Link.link)) \
            .join(Video.links)\
            .join(YoutubeVideo, Video.id == YoutubeVideo.external_id)\
            .filter(YoutubeVideo.description_lang == 'ru').count()

        count_product = session.query(distinct(Link.product_domain))\
            .join(Video.links)\
            .join(YoutubeVideo, Video.id == YoutubeVideo.external_id)\
            .filter(YoutubeVideo.description_lang == 'ru').count()

        return [count_video, count_channel, count_link, count_product]


x = np.array(['video', 'channel', 'links', 'product'])
y = np.array(count_objects())

fig, ax = plt.subplots()

ax.bar(x, y)

ax.set_facecolor('seashell')
fig.set_facecolor('floralwhite')
fig.set_figwidth(12)
fig.set_figheight(6)

plt.show()
