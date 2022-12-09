from django.shortcuts import render, redirect
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from time import strftime
#from django.contrib.auth.forms import UserCreationForm

from Tontine.admin import UserCreationForm


def login_user(request):
    template = 'usertemplate/login.html'
    context = {}

    context['year'] = strftime("%Y")

    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        _user = authenticate(request, username=username, password=password)

        if _user is not None:
            login(request, _user)
            print('login sucessfully')
            return redirect('home')
        else:
            messages.success(
                request, ("There Was an error with authentication"))
            return redirect('login')

    return render(request, template, context)


def register(request):
    template = 'usertemplate/register.html'
    context = {}

    if request.method == 'POST':
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            _user = authenticate(request, username=email, password=password)
            login(request, _user)
            return redirect('home')
        else:
            messages.success(
                request, ("There Was an error with authentication"))
            return redirect('register')
    form = UserCreationForm

    context['form'] = form

    return render(request, template, context)


def logout_user(request):
    logout(request)
    return redirect('home')
