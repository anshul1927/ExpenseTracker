from django.urls import path
from . import views

urlpatterns = [
    path('create_group/', views.create_group.as_view()),
    path('get_user_group/', views.get_group_data_for_user.as_view()),
    path('get_group_detail/', views.get_group_detail.as_view()),
    path('delete_group/', views.delete_group.as_view()),
    path('debts/', views.UserGroupTotalDebt),
   # path('users/', views.AddUserToGroup.as_view()),
]
