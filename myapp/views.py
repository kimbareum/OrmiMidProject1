from django.shortcuts import render
from django.views import View

from .utils.utils import get_banner


class IndexMain(View):

    def get(self, request):

        context = {
            'title': '인덱스 페이지',
            'banner': get_banner(main="Welcome"),
        }
        return render(request, 'index.html', context)


class Error(View):
    
    def get(self,request):
        context = {
            "banner": get_banner(text="Something Went Wrong..."),
        }
        return render(request, 'error.html')