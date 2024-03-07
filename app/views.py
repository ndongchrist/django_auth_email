from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, "app/index.html")

def register(request):
    return render(request, 'app/register.html')

def login(request):
    return render(request, 'app/login.html')

def logout(request):
    pass
    # return render(request, 'app/logout.html')