from django.urls import path

# from . import views # views 디렉터리의 __init__.py 파일에서모든 뷰 파일의 함수를 import 했기 때문에 urls.py와 같은 다른 모듈에서 views 모듈의 함수를 사용하는 부분을 수정할 필요가 없다.
from . import views

# 네임스페이스
app_name = 'srt'

urlpatterns = [
    path('', views.index, name='index'),                        # 디폴트로 index에 연결 (www.host/srt 일 때)
    path('trainlist', views.trainlist, name='trainlist'),       # www.host/trainlist 일 때
]
