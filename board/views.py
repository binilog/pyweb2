from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.utils import timezone
from pyexpat.errors import messages
from django.core.paginator import Paginator

from board.models import Question, Answer, Comment
from board.forms import QuestionForm, AnswerForm, CommentForm


def index(request):
    
    page = request.GET.get('page', '1')
    # 질문 목록
    # question_list = Question.objects.all()  #db 전체조회
    question_list = Question.objects.order_by('-create_date')

    # 작성일 기준 내림차순(- 기호 사용)
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj}
    return render(request, 'board/question_list.html',
                  context)
    # return HttpResponse("pyweb 사이트 입니다.")


def detail(request, question_id):
    # 질문/답변 상세
    # question = Question.objects.get(id=question_id) #해당 id의 질문
    question = get_object_or_404(Question, pk=question_id)
    # 경로에 오류가 있을 때 404로 처리(페이지가 없음)
    return render(request, 'board/detail.html', {'question': question})


@login_required(login_url='common:login')  # 로그인이 안되어 있으면 로그인 페이지로 이동
def question_create(request):
    # 질문 등록
    if request.method == "POST":
        form = QuestionForm(request.POST)  # 자료 전달받음(request.POST)
        if form.is_valid():
            question = form.save(commit=False)  # 가저장(날짜가 없어서 가저장)
            question.create_date = timezone.now()  # 날짜 시간 저장
            question.author = request.user  # 글쓴이에 세션 저장
            question.save()  # 실제 저장
            return redirect('board:index')  # 이동할 경로(앱 네임사용) 저장
    else:
        form = QuestionForm()  # form 객체 생성
    return render(request, 'board/question_form.html', {'form': form})


@login_required(login_url='common:login')
def answer_create(request, question_id):
    # 답변 등록
    # question = Question.objects.get(id=question_id) #해당 id의 질문 객체 생성
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)  # 입력값 전달받음
        if form.is_valid():
            answer = form.save(commit=False)  # 내용만 저장됨
            answer.create_date = timezone.now()  # 작성일
            answer.author = request.user  # 세션 발급
            answer.question = question  # 외래키 질문 저장
            answer.save()
            return redirect('board:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'board/detail.html', context)


@login_required(login_url='common:login')
def question_modify(request, question_id):
    # 질문 수정
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)  # 수정된 질문 가저장
            question.author = request.user  # 세션 발급
            question.modify_date = timezone.now()  # 수정일
            question.save()
            return redirect('board:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)  # instance를 쓰면 폼에 내용이 채워짐
    return render(request, 'board/question_form.html', {'form': form})


@login_required(login_url='common:login')
def question_delete(request, question_id):
    # 질문 삭제
    question = get_object_or_404(Question, pk=question_id)
    question.delete()  # 질문 삭제
    return redirect('board:index')


#                               답변 라인

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        return redirect('pybo:detail', question_id=answer.question.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('board:detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'board/answer_form.html', context)


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '')
    else:
        answer.delete()
    return redirect('board:detail', question_id=answer.question.id)

#                     댓글 쓰기


@login_required(login_url='common:login')
def comment_create_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.question = question
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('board:detail', question_id=comment.question.id), comment.id))
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'board/comment_form.html', context)

#                     수정 라인


@login_required(login_url='common:login')
def comment_modify_question(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, 'Unknown')
        return redirect('board:detail', question_id=comment.question.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('board:detail', question_id=comment.question.id), comment.id))
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'board/comment_form.html', context)

#                    삭제 라인


@login_required(login_url='common:login')
def comment_delete_question(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '404')
        return redirect('board:detail', question_id=comment.question_id)
    else:
        comment.delete()
    return redirect('board:detail', question_id=comment.question_id)


def vote():
    return None