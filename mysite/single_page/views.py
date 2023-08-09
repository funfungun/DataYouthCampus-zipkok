from django.shortcuts import render

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