from django.urls import path
from . import views

urlpatterns = [
    path('one/', views.one),
    path('two/', views.two),
    path('three/', views.three),
    path('', views.index),
]