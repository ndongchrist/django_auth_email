from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    return render(request, "app/index.html")

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']

        my_user = User.objects.create_user(username, email, password)
        my_user.first_name = firstname
        my_user.last_name = lastname
        my_user.save()

        messages.success(request, 'Account Successfully Created')
        return redirect('login')
    else:
        pass

    return render(request, 'app/register.html')

def logIn(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            firstname = user.first_name
            messages.success(request, f"{firstname} Login was sucessful")
            return render(request, 'app/index.html', {'firstname': firstname})
        else:
            messages.error(request, "Login Unsucessful")
            return redirect('home')
    return render(request, 'app/login.html')


def logOut(request):
    logout(request)
    messages.success(request, "Logout sucessful")
    return redirect('home')
    # return render(request, 'app/logout.html')