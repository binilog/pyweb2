from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from board.models import Comment


class UserForm(UserCreationForm):  # 부모 필드(username, password1, password2)
    email = forms.EmailField()  # 추가 필드

    class Meta:
        model = User
        fields = ('username', 'email')  # 튜플 구조임


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }
