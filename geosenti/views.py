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
    input = request.POST['searched']
    a = starter(input)
    return JsonResponse({'success':'success'})
# Create your views here.
