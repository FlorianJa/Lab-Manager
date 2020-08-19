from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'pay_by_use\index.html')
