from django.urls import path
from board import views

app_name = 'board'  #네임 스페이스 설정

urlpatterns = [
    #127.0.0.1:8000/board/
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail')
]