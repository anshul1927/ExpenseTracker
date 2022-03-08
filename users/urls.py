from django.urls import path, include
from users import views
from django.urls import re_path

from users.views import getUserList

urlpatterns = [
    path('createUser', views.CreateUserAPIView.as_view(), name="createUser"),
    path('get_users', views.getUserList.as_view(), name="get_users"),
    path('signin', views.signIn.as_view(), name="signin"),
    path('logout', views.LogoutView.as_view(), name="logout"),
    path('user', views.UserView.as_view(), name="user"),
    path("<int:pk>/profile", views.Profile.as_view(), name='profile')
]
