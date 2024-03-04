from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from .models import User, Seller







def registerUSeller(request):
    context = {}

    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        uname = request.POST.get('username')
        pwd = request.POST.get('pwd')
        email = request.POST.get('email')
        User.objects.create(
            username= uname,
            password=make_password(pwd),
            email=email,
            phone =  request.POST.get('phone'),
            first_name = request.POST.get('fname'),
            last_name = request.POST.get('lname'),

        )

        user = authenticate(email=email, password=pwd)
        if user:
            login(request, user)
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
        return redirect(index)
    
    return render(request, 'storefront/register-seller.html',context)


@login_required
def sellerProfile(request):
    context = {}
    try:
        seller = Seller.objects.get(user=request.user)
        context['seller'] = seller
    except:
        return redirect('index')
    
    return render(request, 'storefront/seller-profile.html', context)
    








# Create your views here.
