from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'common'

urlpatterns = [
    # 기본적으로 LoginView는 registration이라는 템플릿 디렉터리에서 login.html 파일을 찾는다.
    # 하지만 common 디렉터리에서 템플릿을 관리하고 싶기 때문에 template_name을 따로 지정한다.
    # 함수에서 템플릿에 User 객체를 전달하지 않더라도 템플릿에서는 django.contrib.auth 기능으로 인해 User 객체를 사용할 수 있다. 대표적으로 다음과 같은 것들이 있다. : user.is_authenticated / user.is_anonymous / user.username / user.is_superuser   
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),

]