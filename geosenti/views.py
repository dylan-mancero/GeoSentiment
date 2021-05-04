from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from geosenti.methods import starter

def index(request):
    context = {
        'hello':'hello',
    }
    return render(request,'geosenti/home.html',context)
def search(request):

    input = request.POST['searched']
    country1 = request.POST['country1']
    country2 = request.POST['country2']

    leftData, rightData = starter(input, country1, country2)
    print(str(leftData))
    print(str(rightData))
    return JsonResponse({
        'success':'success',
        'left':leftData,
        'right':rightData
    })
# Create your views here.
