from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from .models import User, Seller




def index(request):
    return render(request, 'storefront/index.html')


def registerUSeller(request):
    context = {}

    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        User.objects.create(
            username=request.POST.get('username'),
            password=make_password(request.POST.get('pwd')),
            email=request.POST.get('email'),
            phone =  request.POST.get('phone'),
            first_name = request.POST.get('fname'),
            last_name = request.POST.get('lname'),

        )
        messages.success(request, 'Registered Successfully')
        return redirect(registerSeller)



    return render(request, 'storefront/register-u-seller.html', context)

@login_required
def registerSeller(request):
    context = {}

    if request.method == 'POST':
        Seller.objects.create(
            user = request.user,
            store_name = request.POST.get('sname'),
            desc = request.POST.get('desc'),

        )
        messages.success(request, 'Registered Successfully')
        return redirect(registerSeller)
    
    return render(request, 'storefront/register-seller.html',context)








# Create your views here.
