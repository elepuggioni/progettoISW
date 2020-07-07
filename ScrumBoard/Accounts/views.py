from django.shortcuts import render, redirect
from django.http import HttpResponse
from ScrumBoard import *
from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
from .models import *
from .forms import CreateUserForm

def registerPage(request):
    form = CreateUserForm

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'L\'account di ' + user + 'è stato creato con successo!' )
            return redirect('login')

    context = {'form': form}
    return render(request, 'register.html', context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request,'Username o password errati')

    context = {}
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def home(request):
    return render(request, 'dashboard.html')

def profilo(request):
    return render(request, 'profilo.html')