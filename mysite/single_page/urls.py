from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    
    path('autonomous/', views.first, name='first'),
    path('price/', views.autonomous, name='autonomous'),
    path('category/', views.price, name='price'),
    path('input/', views.category, name = 'category'),
    path('result/',views.final_page,name='final_page'),
    # path('last/', views.qq, name = 'qq'),
    #path('check_and_filter/',views.check_and_filter,name='check_and_filter'),
    # path('input/',views.final_page,name='final_page'),
    # path('result/',views.final_page,name ='final_page'),
]