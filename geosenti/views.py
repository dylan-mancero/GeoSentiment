from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from geosenti.methods import starter

def index(request):
    context = {
        'hello':'hello',
    }
    return render(request,'geosenti/home.html',context)
def search(request):
    print(request.POST['searched'])
    print(request.POST['country1'])
    print(request.POST['country2'])

    input = request.POST['searched']
    country1 = request.POST['country1']
    country2 = request.POST['country2']

    britishScore, usaScore = starter(input, country1, country2)
    print(str(britishScore))
    return JsonResponse({
        'success':'success',
        'left':britishScore,
        'right':usaScore
    })
# Create your views here.
