# CONFIGS FOR RABBITMQ

RABBITMQ_HOST = '34.102.26.251'
RABBITMQ_PORT = 5672
RABBITMQ_VHOST = '/'
RABBITMQ_LOGIN = 'mazan'
RABBITMQ_PASSWORD = 'mazan'

RABBITMQ_URL = f'''amqp://{RABBITMQ_LOGIN}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}'''

# CONFIGS FOR REDIS

REDIS_HOST = '35.247.62.69'
REDIS_PORT = 6379
REDIS_USERNAME = 'user'
REDIS_PASSWORD = 'LYWxyNDJSg7h'

REDIS_URL = f'''redis://{REDIS_USERNAME}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}'''

# CONFIGS FOR POSTGRESQL_FIRST

POSTGRES_HOST_FIRST = '10.63.16.40'
POSTGRES_PORT_FIRST = 5432
POSTGRESS_DB_FIRST = 'postgres'
POSTGRES_LOGIN_FIRST = 'postgres'
POSTGRES_PASSWORD_FIRST = 'pLD30qaJr7tc5rlk'

POSTGRES_URL_FIRST = f'postgresql://{POSTGRES_LOGIN_FIRST}:{POSTGRES_PASSWORD_FIRST}@{POSTGRES_HOST_FIRST}:{POSTGRES_PORT_FIRST}/{POSTGRESS_DB_FIRST}'

# CONFIGS FOR POSTGRESQL_SECOND

POSTGRES_HOST_SECOND = '10.63.16.34'
POSTGRES_PORT_SECOND = 5432
POSTGRESS_DB_SECOND = 'oxicore-video-products'
POSTGRES_LOGIN_SECOND = 'postgres'
POSTGRES_PASSWORD_SECOND = 'zPc0HxpCfHxpNu0D'

POSTGRES_URL_SECOND = f'postgresql://{POSTGRES_LOGIN_SECOND}:{POSTGRES_PASSWORD_SECOND}@{POSTGRES_HOST_SECOND}:{POSTGRES_PORT_SECOND}/{POSTGRESS_DB_SECOND}'
