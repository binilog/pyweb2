from django.urls import path

from polls import views

app_name = 'poll'

urlpatterns = [
    path('', views.index, name='index'),

]