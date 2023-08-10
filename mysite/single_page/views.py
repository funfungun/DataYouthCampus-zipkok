from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from rest_framework.decorators import api_view
from .models import DataEngCsv
from .serializers import TestDataSerializer

def pp(request):
    latest_list = DataEngCsv.objects.all()
    template = loader.get_template('single_page/pp.html')
    context = {'latest_list': latest_list}
    return HttpResponse(template.render(context, request))

def getTestDatas(request):
    datas = DataEngCsv.objects.all()
    serializer = TestDataSerializer(datas, many=True)
    return HttpResponse(serializer.data)

def index(request):
    return render(
        request,
        'single_page/index.html'
    )


def one(request):
    return render(
        request,
        'single_page/one.html'
    )

def two(request):
    return render(
        request,
        'single_page/two.html'
    )

def three(request):
    return render(
        request,
        'single_page/three.html'
    )