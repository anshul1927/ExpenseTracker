from django.urls import path, include
from . import views

urlpatterns = [
    path('create_group/', views.create_group.as_view(), name='createGroup'),
    path('get_user_group/', views.get_group_data_for_user.as_view(), name='getUserGroup'),
    path('get_group_detail/', views.get_group_detail.as_view(), name='getGroupDetail'),
    path('delete_group/', views.delete_group.as_view(), name='deleteGroup'),
    path('remove_member/', views.remove_member_from_group.as_view(), name='removeMember'),
    path('add_member/', views.add_new_member.as_view(), name='addMember'),
    path('<int:id>/debts/', views.UserGroupDebts.as_view()),
    # path('<int:id>/debts/pay/', views.Pay.as_view()),
    path('<int:id>/expense/', include('expenses.urls'))
]
