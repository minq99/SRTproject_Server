from django.contrib import admin
from .models import Question

# 관리자에게 model을 등록하면 ~/admin 사이트에서 관리 가능
admin.site.register(Question)

# QuestionAdmin 클래스: Question 모델에 세부 기능을 추가할 수 있는 클래스
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']


# 추가 기능: https://docs.djangoproject.com/en/4.0/ref/contrib/admin/