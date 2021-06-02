import logging

from sqlalchemy import insert
import sqlalchemy.exc as exc

from db.models import *


def add_youtube_video(video, db_session_insert):
    try:
        db_session_insert.add(video)
        db_session_insert.flush()
    except (exc.IntegrityError, exc.PendingRollbackError):
        logging.info("Integrity Error")
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
    except (exc.IntegrityError, exc.PendingRollbackError):
        logging.info("Integrity Error")
    except Exception as e:
        db_session_insert.rollback()
        raise e
    except TimeoutError:
        db_session_insert.close()


def add_link(link, db_session_insert):
    try:
        db_session_insert.add(link)
        db_session_insert.flush()
    except (exc.IntegrityError, exc.PendingRollbackError):
        logging.info("Integrity Error")
    except Exception as e:
        db_session_insert.rollback()
        raise e
    except TimeoutError:
        db_session_insert.close()


def add_product(product, db_session_insert):
    try:
        db_session_insert.add(product)
        db_session_insert.flush()
    except (exc.IntegrityError, exc.PendingRollbackError):
        logging.info("Integrity Error")
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
    except (exc.IntegrityError, exc.PendingRollbackError):
        logging.info("Integrity Error")
    except Exception as e:
        db_session_insert.rollback()
        raise e


def add_email(email, db_session_insert):
    try:
        db_session_insert.add(email)
        db_session_insert.flush()
    except (exc.IntegrityError, exc.PendingRollbackError):
        logging.info("Integrity Error")
    except Exception as e:
        db_session_insert.rollback()
        raise e
    except TimeoutError:
        db_session_insert.close()


def update_product(product_domain, product_data, db_session_insert):
    try:
        db_session_insert.query(Product).filter(Product.domain == product_domain).update(product_data)
        db_session_insert.flush()
    except (exc.IntegrityError, exc.PendingRollbackError):
        logging.info("Integrity Error")
    except Exception as e:
        db_session_insert.rollback()
        raise e


def update_youtube_video(video_id, video_data, db_session_insert):
    try:
        db_session_insert.query(YoutubeVideo).filter(YoutubeVideo.id == video_id).update(video_data)
        db_session_insert.flush()
    except (exc.IntegrityError, exc.PendingRollbackError):
        logging.info("Integrity Error")
    except Exception as e:
        db_session_insert.rollback()
        raise e
