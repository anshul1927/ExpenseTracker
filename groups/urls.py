from django.urls import path
from . import views

urlpatterns = [
    path('', views.GroupsList.as_view()),
    path('<int:id>/', views.GroupDetails.as_view()),
    path('<int:id>/users/', views.GroupUsersList.as_view()),
    path('users/', views.AddUserToGroup.as_view()),
]
