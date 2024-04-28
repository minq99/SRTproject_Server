from django.urls import path

# from . import views # views 디렉터리의 __init__.py 파일에서모든 뷰 파일의 함수를 import 했기 때문에 urls.py와 같은 다른 모듈에서 views 모듈의 함수를 사용하는 부분을 수정할 필요가 없다.
from .views import base_views, question_views, answer_views



# 네임스페이스
app_name = 'main'

urlpatterns = [
    # base_views.py
    path('', base_views.index, name='index'),                                                      # 디폴트로 index에 연결 (www.host/main 일 때)
    path('<int:question_id>/', base_views.detail, name='detail'),                                  # 뒤에 숫자가 붙었을 때 (www.host/main/{n} 일 때)

    # question_views.py
    path('question/create/', question_views.question_create, name='question_create'),
    path('question/modify/<int:question_id>/', question_views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/', question_views.question_delete, name='question_delete'),
    path('question/vote/<int:question_id>/', question_views.question_vote, name='question_vote'),

    # answer_views.py
    path('answer/create/<int:question_id>/', answer_views.answer_create, name='answer_create'),      # www.host/main/answer/create/{n}일 때
    path('answer/modify/<int:answer_id>/', answer_views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/', answer_views.answer_delete, name='answer_delete'),        # www.host/main/login 일 때


]
