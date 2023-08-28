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
    path('result/03091/',views.o3091,name='03091'),
    path('result/03106/',views.o3106,name='03106'),
    path('result/03633/',views.o3633,name='03633'),
    path('result/03757/',views.o3757,name='03757'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)