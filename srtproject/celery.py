# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Django의 settings 모듈을 Celery의 기본 설정으로 사용하도록 합니다.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'srtproject.settings.prod')

app = Celery('srtproject')

# 여기서 문자열을 사용하는 이유는 작업자를 위한 비동기성을 직렬화할 필요가 없기 때문입니다.
# 이름을 정의하지 않으면 Celery는 기본적인 설정 모듈로 'celery'를 사용합니다.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Django의 모든 설정 모듈을 Celery의 설정으로 로드합니다.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')