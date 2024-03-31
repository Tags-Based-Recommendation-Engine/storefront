from django.shortcuts import render, redirect
from django.contrib.auth import login, logout , authenticate
from django.contrib.auth.decorators import login_required
from storefront.models import Product, Category


def index(request):
    product = Product.objects.all()
    Catagory = Category.objects.all()
    context = {
        'product':product,
        'catagory' : Catagory
    }
    return render(request, 'market/index.html', context)

def search(request):
    return render(request, 'market/search.html')

def cart(request):
    return render(request, 'market/cart.html')

def product(request):
    return render(request, 'market/product.html')

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('index')