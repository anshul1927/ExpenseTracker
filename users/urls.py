from django.urls import path, include
from users import views
from django.urls import re_path

from users.views import getUserList

urlpatterns = [
    path('createUser', views.CreateUserAPIView.as_view()),
    path('get_users', getUserList.as_view())
]
