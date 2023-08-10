from django.shortcuts import render

def landing(request):
    return render(
        request,
        'single_page/landing.html'
    )


def about_me(request):
    return render(
        request,
        'single_page/about_me.html'
    )

# from ..board.views import DataEngCsv
# # board 폴더에서 views파일에 있는 DataEngCsv 클래스 사용

# def test_2(request):
#     zip_code = DataEngCsv.objects.first()
#     context = {'zipcode':zip_code}

#     return render(request,'single-page/landing.html',context)

