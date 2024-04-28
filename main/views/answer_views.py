from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect ,resolve_url
from django.utils import timezone

from ..forms import AnswerForm
from ..models import Question, Answer

@login_required(login_url='common:login')  # 로그인 안한사람은 함수가 실행되지 않고 login url 타도록.
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    # form data가 아닐때
        # question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())         # content=request.POST.get('content'): POST로 전송된 폼(form) 데이터 항목 중 content 값을 의미한다.
        # OR
        # answer = Answer(question=question, content=request.POST.get('content'), create_date=timezone.now())
        # answer.save()

    # form data로 받을때
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user  # author 속성에 로그인 계정 저장
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('{}#answer_{}'.format( resolve_url('main:detail', question_id=question.id), answer.id))

    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'main/question_detail.html', context)

@login_required(login_url='common:login')
def answer_modify(request, answer_id):

    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('main:detail', question_id=answer.question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('{}#answer_{}'.format(resolve_url('main:detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'main/answer_form.html', context)


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('main:detail', question_id=answer.question.id)


