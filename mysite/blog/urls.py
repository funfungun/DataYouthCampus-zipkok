from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view()),
    # path('',views.index),
    path('<int:pk>/', views.PostList.as_view()),
]