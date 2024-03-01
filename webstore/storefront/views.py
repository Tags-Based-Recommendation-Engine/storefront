from django.shortcuts import render, redirect
from django.contrib.auth import login, logout , authenticate
from django.contrib.auth.decorators import login_required



def index(request):
    return render(request, 'storefront/index.html')

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('index')

# Create your views here.
