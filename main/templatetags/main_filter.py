import markdown
from django import template
from django.utils.safestring import mark_safe


register = template.Library()

# 기존 값 value에서 입력으로 받은 값 arg를 빼서 리턴하는 함수
@register.filter
def sub(value, arg):
    return value - arg



@register.filter
def mark(value):
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))