from .base import *

ALLOWED_HOSTS = ['13.209.12.46']

# STATIC_ROOT is useless during development, it's only required for deployment. -> Because Django knows where static files are.
# But Nginx doesn't know anything about my Django project and doesn't know where to find static files.
# So i need to tell Nginx to look for static files in STATIC_ROOT
STATIC_ROOT = BASE_DIR / 'static/'

# STATICFILES_DIRS는 운영에는 비워놔야함. 
# 이 오류 때문에 : The STATICFILES_DIRS setting should not contain the STATIC_ROOT setting.
STATICFILES_DIRS = []


