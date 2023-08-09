from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse  # 추가


def index(request):  # 추가
    return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.")