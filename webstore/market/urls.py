from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/<str:query>', views.search, name='search'),
    path('cart/', views.cart, name='cart'),
    path('<str:slug>', views.product, name='product'),
    path('logout', views.logoutUser, name='logout'),
]