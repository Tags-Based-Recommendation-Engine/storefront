from django.shortcuts import render, redirect
from django.contrib.auth import login, logout , authenticate
from django.contrib.auth.decorators import login_required


def index(request):
    context = {}
    return render(request, 'market/index.html', context)

def search(request):
    return render(request, 'market/search.html')

def cart(request):
    return render(request, 'market/cart.html')

def product(request):
    return render(request, 'market/product.html')

def sellerRegister(request):
    return render(request, 'registeration/seller.html')

def userRegister(request):
    return render(request, 'registeration/user.html')

def Login(request):
    return render(request, 'registeration/login.html')

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('index')