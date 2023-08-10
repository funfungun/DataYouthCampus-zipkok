from django.urls import path
from . import views

urlpatterns = [
    path('board01/', views.getTestDatas),
]