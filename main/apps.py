from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main' # 디폴트로는 MainConfig 이라고 되어있었음