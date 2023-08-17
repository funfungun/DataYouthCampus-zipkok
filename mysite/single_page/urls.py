from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('check_and_filter/',views.first, name = 'first'),
    path('category/',views.check_and_filter, name='check_and_filter'),
    path('input/',views.category,name='category'),
    path('result/',views.final_page,name='final_page'),
]