from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index),
    path('check_and_filter/',views.first, name = 'first'),
    path('category/',views.check_and_filter, name='check_and_filter'),
    path('input/',views.category,name='category'),
    path('result/',views.final_page,name='final_page'),
    path('result/image/',views.image,name='image'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)