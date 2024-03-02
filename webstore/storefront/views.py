from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required



def index(request):
    return render(request, 'storefront/index.html')


def registerSeller(request):
    context = {}

    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'storefront/register-seller.html', context)




# Create your views here.
