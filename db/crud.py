import logging

from sqlalchemy import insert
import sqlalchemy.exc as exc

from db.models import *


"""
################################################
# Functions for adding objects to the database #
################################################
"""


def add_object(obj, db_session_insert):
    try:
        db_session_insert.add(obj)
        db_session_insert.flush()
    except Exception as e:
        if isinstance(e, exc.IntegrityError):
            logging.info("Integrity Error")
        elif isinstance(e, exc.PendingRollbackError):
            logging.info("Pending Rollback Error")
        else:
            logging.info("Unknown Error")

        logging.info("Pending Rollback Error")


def add_videolink(video_id, link_id, db_session_insert):
    try:
        data = insert(VideoLink).values(video_id=video_id, link_id=link_id)
        db_session_insert.execute(data)
        db_session_insert.flush()
    except Exception as e:
        if isinstance(e, exc.IntegrityError):
            logging.info("Integrity Error")
        elif isinstance(e, exc.PendingRollbackError):
            logging.info("Pending Rollback Error")
        else:
            logging.info("Unknown Error")

        logging.info("Pending Rollback Error")


"""
##################################################
# Functions for updating objects to the database #
##################################################
"""


def update_product(product_domain, product_data, db_session_insert):
    try:
        db_session_insert.query(Product).filter(Product.domain == product_domain).update(product_data)
        db_session_insert.flush()
    except Exception as e:
        if isinstance(e, exc.IntegrityError):
            logging.info("Integrity Error")
        elif isinstance(e, exc.PendingRollbackError):
            logging.info("Pending Rollback Error")
        else:
            logging.info("Unknown Error")

        logging.info("Pending Rollback Error")


def update_youtube_video(video_id, video_data, db_session_insert):
    try:
        db_session_insert.query(YoutubeVideo).filter(YoutubeVideo.id == video_id).update(video_data)
        db_session_insert.flush()
    except Exception as e:
        if isinstance(e, exc.IntegrityError):
            logging.info("Integrity Error")
        elif isinstance(e, exc.PendingRollbackError):
            logging.info("Pending Rollback Error")
        else:
            logging.info("Unknown Error")

        logging.info("Pending Rollback Error")


"""
##################################################
# Functions for checking objects to the database #
##################################################
"""


def is_video(video_id, db_session):
    try:
        return db_session.query(
            db_session.query(Video.id).filter_by(id=video_id).exists()
        ).scalar()
    except Exception as e:
        db_session.rollback()
        raise e


def is_youtube_video(youtube_video_id, db_session):
    try:
        return db_session.query(
            db_session.query(YoutubeVideo.id).filter_by(id=youtube_video_id).exists()
        ).scalar()
    except Exception as e:
        db_session.rollback()
        raise e


def is_youtube_channel(youtube_channel_id, db_session):
    try:
        return db_session.query(
            db_session.query(YoutubeChannel.id).filter_by(id=youtube_channel_id).exists()
        ).scalar()
    except Exception as e:
        db_session.rollback()
        raise e


def is_link(link_id, db_session):
    try:
        return db_session.query(
            db_session.query(Link.link).filter_by(link=link_id).exists()
        ).scalar()
    except Exception as e:
        db_session.rollback()
        raise e


def is_product(product_id, db_session):
    try:
        return db_session.query(
            db_session.query(Product.domain).filter_by(domain=product_id).exists()
        ).scalar()
    except Exception as e:
        db_session.rollback()
        raise e
