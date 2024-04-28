from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question

# Create your views here.


@login_required(login_url='common:login')  # 로그인 안한사람은 함수가 실행되지 않고 login url 타도록.
def question_create(request):
    if request.method == 'POST':
        # request.POST를 parameter로 넣고 QuestionForm을 생성할 경우에는 request.POST에 담긴 subject, content 값이 QuestionForm의 subject, content 속성에 자동으로 저장되어 객체가 생성된다.
        form = QuestionForm(request.POST)
        if form.is_valid():  # 폼이 유효하다면
            question = form.save(commit=False)  # 임시 저장하여 question 객체를 리턴받는다.
            question.author = request.user  # author 속성에 로그인 계정 저장
            question.create_date = timezone.now()  # 실제 저장을 위해 작성일시를 설정한다.
            question.save()  # 데이터를 실제로 저장한다.
            return redirect('main:index')
    else:                                                            # a태그 링크를 통해 페이지를 요청할 경우에는 무조건 GET 방식이 사용
        form = QuestionForm() 
    context = {'form': form}
    return render(request, 'main/question_form.html', context)



@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author: # 해당 질문의 user가 아닌 경우
        messages.error(request, '수정권한이 없습니다')
        return redirect('main:detail', question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question) # instance를 기준으로 QuestionForm을 생성하지만 request.POST의 값으로 덮어쓰라는 의미
        if form.is_valid():
            question = form.save(commit=False) 
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('main:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'main/question_form.html', context) # 질문등록 페이지로


@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('main:detail', question_id=question.id)
    question.delete()
    return redirect('main:index')

@login_required(login_url='common:login')
def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        question.voter.add(request.user)
    return redirect('main:detail', question_id=question.id)