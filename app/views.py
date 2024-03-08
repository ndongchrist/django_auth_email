from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from authentification.info import *
from django.core.mail import send_mail, EmailMessage
from .token import generatorToken

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

        if User.objects.filter(username=username):
            messages.error(request, 'Username already taken')
            return redirect('register')
        if User.objects.filter(email = email):
            messages.error(request, 'email already used')
            return redirect('register')
        if not username.isalnum():
            return redirect('register')
        if password != password1:
            messages.error(request, 'Passwords not matching')
            return redirect('register')

        my_user = User.objects.create_user(username, email, password)
        my_user.first_name = firstname
        my_user.last_name = lastname
        my_user.is_active = False
        my_user.save()
        messages.success(request, 'Account Successfully Created')

    #Welcome Email Sender
    

        subject = "Wleocome on GoldenBrain, Django System Login"
        message =  "Welcome "+ my_user.first_name + " " + my_user.last_name + " \n We are proud tu count you amongst our users \n\n\n THank you \n\n GoldenDev"
        from_email = EMAIL_HOST_USER
        to_list = [my_user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)

    #Email Confirmation
        current_site = get_current_site(request)
        email_subject = "Confirm Your Email Address On GoldenBrain"
        message_confirm = render_to_string('emailconfirm.html', {
            'name': my_user.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(my_user.pk)),
            'token': generatorToken.make_token(my_user)
        })
        email = EmailMessage(
            email_subject,
            message_confirm,
            EMAIL_HOST_USER,
            [my_user.email]
        )

        email.fail_silently = False
        email.send()

        return redirect('login')
    else:
        pass

    return render(request, 'app/register.html')

def logIn(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        my_user = User.objects.get(username = username)

        if user is not None:
            login(request, user)
            firstname = user.first_name
            messages.success(request, f"{firstname} Login was sucessful")
            return render(request, 'app/index.html', {'firstname': firstname})
        elif my_user.is_active == False:
            messages.error(request, "You haven't Confirmed your account")
        else:
            messages.error(request, "Login Unsucessful")
            return redirect('home')
    return render(request, 'app/login.html')


def logOut(request):
    logout(request)
    messages.success(request, "Logout sucessful")
    return redirect('home')
    # return render(request, 'app/logout.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None
        messages.error(e)
        return print("Activation Error")
    if user is not None and generatorToken.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your Account has been Successfully Activated, You can connect now')
        return redirect('login')
    else:
        messages.error(request, 'Error Occured, Try later!!!')
        return redirect('home')
