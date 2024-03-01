from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required



def index(request):
    return render(request, 'storefront/index.html')




# Create your views here.
