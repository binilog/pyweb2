from django.shortcuts import render

from polls.models import Question


def index(request):
    question_list = Question.objects.all()
    context = {'question_list': question_list}
    return render(request, 'polls/poll_list.html', context)
