from django import forms
from django.contrib.auth.forms import UserCreationForm
from common.models import SrtUser

class UserForm(UserCreationForm):
    
    # 이메일 등의 속성을 추가하기 위해서는 UserCreationForm 클래스를 상속하여 만들어야 한다.
    email = forms.EmailField(label="이메일")
    korailID = forms.CharField(label="korailID")

    
    class Meta:
        model = SrtUser
        fields = ("username", "password1", "password2", "email", "korailID")

