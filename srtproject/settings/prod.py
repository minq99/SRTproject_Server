from .base import *

ALLOWED_HOSTS = ['13.209.12.46']

# STATIC_ROOT is useless during development, it's only required for deployment. -> Because Django knows where static files are.
# But Nginx doesn't know anything about my Django project and doesn't know where to find static files.
# So i need to tell Nginx to look for static files in STATIC_ROOT
STATIC_ROOT = BASE_DIR / 'static/'

# STATICFILES_DIRS는 운영에는 비워놔야함. 
# 이 오류 때문에 : The STATICFILES_DIRS setting should not contain the STATIC_ROOT setting.
STATICFILES_DIRS = []


DEBUG = False



CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Seoul'  # 필요한 시간대로 변경
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True


