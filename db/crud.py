import logging

from sqlalchemy import insert
import sqlalchemy.exc as exc

from db.models import *


"""
################################################
# Functions for adding objects to the database #
################################################
"""


def add_youtube_video(video, db_session_insert):
    try:
        db_session_insert.add(video)
        db_session_insert.flush()
    except exc.IntegrityError:
        logging.info("Integrity Error")
    except exc.PendingRollbackError:
        logging.info("Pending Rollback Error")
    except Exception as e:
        db_session_insert.rollback()
        raise e
    except TimeoutError:
        db_session_insert.close()


def add_youtube_channel(channel, db_session_insert):
    try:
        db_session_insert.add(channel)
        db_session_insert.flush()
    except exc.IntegrityError:
        logging.info("Integrity Error")
    except exc.PendingRollbackError:
        logging.info("Pending Rollback Error")
    except Exception as e:
        db_session_insert.rollback()
        raise e


def add_video(video, db_session_insert):
    try:
        db_session_insert.add(video)
        db_session_insert.flush()
    except exc.IntegrityError:
        logging.info("Integrity Error")
    except exc.PendingRollbackError:
        logging.info("Pending Rollback Error")
    except Exception as e:
        db_session_insert.rollback()
        raise e
    except TimeoutError:
        db_session_insert.close()


def add_link(link, db_session_insert):
    try:
        db_session_insert.add(link)
        db_session_insert.flush()
    except exc.IntegrityError:
        logging.info("Integrity Error")
    except exc.PendingRollbackError:
        logging.info("Pending Rollback Error")
    except Exception as e:
        db_session_insert.rollback()
        raise e
    except TimeoutError:
        db_session_insert.close()


def add_product(product, db_session_insert):
    try:
        db_session_insert.add(product)
        db_session_insert.flush()
    except exc.IntegrityError:
        logging.info("Integrity Error")
    except exc.PendingRollbackError:
        logging.info("Pending Rollback Error")
    except Exception as e:
        db_session_insert.rollback()
        raise e
    except TimeoutError:
        db_session_insert.close()


def add_videolink(video_id, link_id, db_session_insert):
    try:
        data = insert(VideoLink).values(video_id=video_id, link_id=link_id)
        db_session_insert.execute(data)
        db_session_insert.flush()
    except exc.IntegrityError:
        logging.info("Integrity Error")
    except exc.PendingRollbackError:
        logging.info("Pending Rollback Error")
    except (exc.IntegrityError, exc.PendingRollbackError):
        logging.info("Integrity Error")
    except Exception as e:
        db_session_insert.rollback()
        raise e


def add_email(email, db_session_insert):
    try:
        db_session_insert.add(email)
        db_session_insert.flush()
    except exc.IntegrityError:
        logging.info("Integrity Error")
    except exc.PendingRollbackError:
        logging.info("Pending Rollback Error")
    except Exception as e:
        db_session_insert.rollback()
        raise e
    except TimeoutError:
        db_session_insert.close()


"""
##################################################
# Functions for updating objects to the database #
##################################################
"""


def update_product(product_domain, product_data, db_session_insert):
    try:
        db_session_insert.query(Product).filter(Product.domain == product_domain).update(product_data)
        db_session_insert.flush()
    except exc.IntegrityError:
        logging.info("Integrity Error")
    except exc.PendingRollbackError:
        logging.info("Pending Rollback Error")
    except Exception as e:
        db_session_insert.rollback()
        raise e


def update_youtube_video(video_id, video_data, db_session_insert):
    try:
        db_session_insert.query(YoutubeVideo).filter(YoutubeVideo.id == video_id).update(video_data)
        db_session_insert.flush()
    except exc.IntegrityError:
        logging.info("Integrity Error")
    except exc.PendingRollbackError:
        logging.info("Pending Rollback Error")
    except Exception as e:
        db_session_insert.rollback()
        raise e


"""
##################################################
# Functions for checking objects to the database #
##################################################
"""


def is_video(video_id, db_session):
    try:
        video = db_session.query(Video).filter(Video.id == video_id).scalar()

        if video:
            flag = True
        else:
            flag = False

        return flag
    except Exception as e:
        db_session.rollback()
        raise e


def is_youtube_video(youtube_video_id, db_session):
    try:
        youtube_video = db_session.query(YoutubeVideo).filter(YoutubeVideo.id == youtube_video_id).scalar()

        if youtube_video:
            flag = True
        else:
            flag = False

        return flag
    except Exception as e:
        db_session.rollback()
        raise e


def is_youtube_channel(youtube_channel_id, db_session):
    try:
        youtube_channel = db_session.query(YoutubeChannel.id).filter(YoutubeChannel.id == youtube_channel_id).scalar()

        if youtube_channel:
            flag = True
        else:
            flag = False

        return flag
    except Exception as e:
        db_session.rollback()
        raise e


def is_link(link_id, db_session):
    try:
        link = db_session.query(Link.link).filter(Link.link == link_id).scalar()

        if link:
            flag = True
        else:
            flag = False

        return flag
    except Exception as e:
        db_session.rollback()
        raise e


def is_product(product_id, db_session):
    try:
        product = db_session.query(Product.domain).filter(Product.domain == product_id).scalar()

        if product:
            flag = True
        else:
            flag = False

        return flag
    except Exception as e:
        db_session.rollback()
        raise e
