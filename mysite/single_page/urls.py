from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('autonomous/', views.first, name='first'),
    path('price/', views.autonomous, name='autonomous'),
    path('category/', views.price, name='price'),
    path('qq/', views.category, name = 'category'),
    path('last/', views.qq, name = 'qq'),
]