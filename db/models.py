from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, create_engine
from sqlalchemy.dialects.postgresql import ARRAY, JSON
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import Table
from sqlalchemy.sql import func

from settings import POSTGRES_URL_FIRST


Base = declarative_base()
engine = create_engine(POSTGRES_URL_FIRST)


VideoLink = Table('video_link', Base.metadata,
                  Column('video_id', String, ForeignKey('video.id'), primary_key=True),
                  Column('link_id', String, ForeignKey('link.link'), primary_key=True, index=True))


class Video(Base):
    __tablename__ = 'video'

    id = Column(String, primary_key=True)
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, onupdate=func.now())
    status = Column(Boolean)
    payload = Column(String)

    links = relationship('Link', secondary=VideoLink, backref=backref('videos', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return f"<Video({self.id, self.created_at})>"


class Link(Base):
    __tablename__ = 'link'

    link = Column(String, primary_key=True)
    final_link = Column(String)
    product_domain = Column(String, ForeignKey('product.domain'), index=True)
    code = Column(Integer)
    payload = Column(String)
    is_ad = Column(Boolean)
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, onupdate=func.now())

    def __repr__(self):
        return f"<Link({self.link, self.final_link, self.modified_at, self.product_domain})>"


class Product(Base):
    __tablename__ = 'product'
    domain = Column(String, primary_key=True)
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, onupdate=func.now())
    canonical_domain = Column(String)
    canonical_link = Column(String)
    category = Column(String)
    copyright = Column(String)
    copyright_lang = Column(String)
    copyright_trans = Column(String)
    description = Column(String)
    description_lang = Column(String)
    description_trans = Column(String)
    description_trans_lang = Column(String)
    error = Column(String)
    favicon = Column(String)
    final_url = Column(String)
    h1 = Column(String)
    h1_lang = Column(String)
    h1_trans = Column(String)
    keyphrases = Column(ARRAY(String))
    keywords = Column(ARRAY(String))
    meta_img = Column(String)
    meta_keywords = Column(ARRAY(String))
    meta_keywords_lang = Column(String)
    meta_keywords_trans = Column(ARRAY(String))
    meta_lang = Column(String)
    meta_site_name = Column(String)
    meta_title = Column(String)
    meta_title_lang = Column(String)
    meta_title_trans = Column(String)
    name = Column(String)
    resp_time = Column(Integer)
    socials = Column(JSON)
    status = Column(String)
    summary = Column(String)
    tags = Column(ARRAY(String))
    title = Column(String)
    title_lang = Column(String)
    title_trans = Column(String)
    top_image = Column(String)
    main_text = Column(String)
    html = Column(String)
    external = Column(Boolean)

    links = relationship('Link', backref='product', lazy='dynamic')

    def __repr__(self):
        return f"<Product({self.domain, self.modified_at})>"


class YoutubeVideo(Base):
    __tablename__ = 'youtube_video'

    id = Column(Integer, primary_key=True, unique=True)
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, onupdate=func.now())
    external_id = Column(String(length=50))
    name = Column(String(length=255))
    picture = Column(String(length=200))
    description = Column(String)
    tags = Column(String)
    default_audio_language = Column(String(length=10))
    upload_date = Column(DateTime)
    channel_id = Column(Integer)
    duration_sec = Column(Integer)
    isfamilyfriendly = Column(Boolean)
    game_title = Column(String(length=255))
    category = Column(String(length=64))
    default_language = Column(String(length=10))
    paid_promotion = Column(Boolean)
    gamechannel_external_id = Column(String(length=50))
    game_id = Column(Integer)
    unavailable_status = Column(String(length=64))
    name_trans = Column(String(length=255))
    description_trans = Column(String)
    tags_trans = Column(String)
    main_lang = Column(String)
    description_lang = Column(String)
    name_lang = Column(String)
    tags_lang = Column(String)
    error = Column(String)

    def __repr__(self):
        return f"<YoutubeVideo({self.external_id, self.created_at})>"


class YoutubeChannel(Base):
    __tablename__ = 'youtube_channel'

    id = Column(Integer, primary_key=True, unique=True)
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, onupdate=func.now())
    external_id = Column(String(length=50))
    type = Column(String(length=20))
    name = Column(String(length=200))
    description = Column(String)
    logo = Column(String(length=200))
    country = Column(String(length=200))
    category = Column(String)
    published_date = Column(DateTime)
    uid = Column(String(length=200))
    influencer_id = Column(Integer)
    status = Column(String(length=20))
    language = Column(String(length=200))
    banner = Column(String(length=512))
    c_url = Column(String(length=200))
    user_url = Column(String(length=200))
    verification_badge = Column(String(length=200))
    email_button = Column(Boolean)

    emails = relationship('Email', backref='channel', lazy='dynamic')

    def __repr__(self):
        return f"<YoutubeChannel({self.external_id, self.created_at})>"


class Email(Base):
    __tablename__ = 'email'

    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, ForeignKey('youtube_channel.id'))
    channel_description = Column(String)
    video_description = Column(String)

    def __repr__(self):
        return f"<Email({self.id, self.channel_id})>"


if __name__ == "__main__":
    Base.metadata.create_all(engine)
