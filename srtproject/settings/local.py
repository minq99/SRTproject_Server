from .base import *
# base.py 파일과 동일하지만 ALLOWED_HOSTS만 다르게 설정하겠다는 의미이다.
ALLOWED_HOSTS = []

# Celery settings
# CELERY_BROKER_URL = 'amqp://localhost'  # RabbitMQ 브로커 URL
# CELERY_RESULT_BACKEND = 'rpc://'   # 결과를 저장할 백엔드 설정 (예: 'rpc://' 또는 'redis://localhost:6379/0')

CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Seoul'  # 필요한 시간대로 변경
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True


