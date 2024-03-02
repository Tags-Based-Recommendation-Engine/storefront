from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('register/seller/1', views.registerUSeller, name='reguseller'),
    path('register/seller/2', views.registerSeller, name='regseller'),
    path('seller/profile', views.sellerProfile, name='sellerprofile'),



]
