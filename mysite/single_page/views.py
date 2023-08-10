from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import DataEngCsv
from .serializers import TestDataSerializer

@api_view(['GET'])

def pp(request):
    datas = DataEngCsv.objects.filter(daiso = 1)
    return render(
        request,
        'single_page/pp.html'
    )

def getTestDatas(request):
    datas = DataEngCsv.objects.all()
    serializer = TestDataSerializer(datas, many=True)
    return Response(serializer.data)

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