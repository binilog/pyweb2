from django.contrib.auth.models import User
from django.db import models

class Question(models.Model):
    objects = None
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)  #제목 칼럼
    content = models.TextField()                #질문 내용
    create_date = models.DateTimeField()        #질문 작성일
    modify_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.subject

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE) #외래키, 제목
    content = models.TextField()          #답변 내용
    create_date = models.DateTimeField()  #답변 작성일
    modify_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.content

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)