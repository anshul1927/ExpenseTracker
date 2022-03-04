from django.urls import path
from . import views

urlpatterns = [
    path('', views.ExpenseList.as_view()),
    path('<int:id>/', views.ExpenseUsers.as_view()),
]