from django.urls import path
from . import views

urlpatterns = [
    path('todos/', views.todo_create),
    path('todos/<int:id>/', views.todo_detail),
    path('users/<int:id>/', views.user_detail),
]
