from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from common.forms import UserForm
from polls.models import Question


def signup(request):
    #회원 가입
    if request.method == "POST":
        form = UserForm(request.POST) #입력값을 가져옴
        if form.is_valid():
            form.save()  #실제 저장
            #가입후 자동 로그인
            username = form.cleaned_data.get('username')  #전달받은 사용자ID 가져옴
            password = form.cleaned_data.get('password1') #전달받은 비밀번호를 가져옴
            user = authenticate(username=username, password=password)  #세션(인증) 발급
            login(request, user)                     #로그인
            return redirect('board:index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form':form})

def index(request):
    question_list = Question.objects.all()
    return render(request, 'poll/index.html', {'question_list':question_list})


