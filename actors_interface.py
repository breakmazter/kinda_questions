import dramatiq
from dramatiq.middleware import TimeLimitExceeded
from dramatiq.results import Results, ResultTimeout
from dramatiq.results.backends import RedisBackend
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from settings import REDIS_PORT, REDIS_HOST, REDIS_PASSWORD, RABBITMQ_URL

broker = RabbitmqBroker(url=RABBITMQ_URL)
result_backend = RedisBackend(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
broker.add_middleware(Results(backend=result_backend))
dramatiq.set_broker(broker)


def should_retry(retries_so_far, exception):
    return retries_so_far < 3 and not (isinstance(exception, TimeLimitExceeded) or isinstance(exception, ResultTimeout))


@dramatiq.actor(queue_name='josef_create_youtube_video_josef',
                store_results=False, max_retries=3, time_limit=180000, retry_when=should_retry)
def create_youtube_video(youtube_video_id):
    pass


@dramatiq.actor(queue_name='josef_create_youtube_channel_josef',
                store_results=False, max_retries=3, time_limit=180000, retry_when=should_retry)
def create_youtube_channel(channel_id):
    pass


@dramatiq.actor(queue_name='josef_create_link_josef',
                store_results=False, max_retries=3, time_limit=180000, retry_when=should_retry)
def create_link(video_id):
    pass


@dramatiq.actor(queue_name='josef_create_product_josef',
                store_results=False, max_retries=3, time_limit=180000, retry_when=should_retry)
def create_product(video_id):
    pass


@dramatiq.actor(queue_name='josef_update_product_description_josef',
                store_results=False, max_retries=3, time_limit=180000, retry_when=should_retry)
def update_product_description(product_domain, product_data):
    pass


@dramatiq.actor(queue_name='josef_update_video_tags_josef',
                store_results=False, max_retries=3, time_limit=180000, retry_when=should_retry)
def update_video_tags(product_domain):
    pass


@dramatiq.actor(queue_name='josef_delete_video_josef',
                store_results=False, max_retries=3, time_limit=180000, retry_when=should_retry)
def delete_video(video_id):
    pass


@dramatiq.actor(queue_name='josef_create_email_josef',
                store_results=False, max_retries=3, time_limit=180000, retry_when=should_retry)
def create_email(channel_id):
    pass
