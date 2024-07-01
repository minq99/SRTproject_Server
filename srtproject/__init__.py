# __init__.py
#  Celery를 초기화합니다.
from __future__ import absolute_import, unicode_literals

# 이 파일을 Celery 앱에 불러옵니다.
from .celery import app as celery_app

__all__ = ('celery_app',)