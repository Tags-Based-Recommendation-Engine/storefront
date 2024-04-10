from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from .models import User, Seller
from market.views import index
from plotly.offline import plot
import plotly.graph_objs as go


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



def update_user_pie():
    # Dummy data for users
    users = [{'username': 'User A', 'user_count': 5}, {'username': 'User B', 'user_count': 3}, {'username': 'User C', 'user_count': 7}]

    # Create data trace for the pie chart
    data = [
        go.Pie(
            labels=[user['username'] for user in users],  # Labels: usernames
            values=[user['user_count'] for user in users]  # Values: count of each user
        )
    ]

    # Define layout for the pie chart
    layout = go.Layout(title='User Distribution')

    # Create figure
    fig = go.Figure(data=data, layout=layout)

    # Generate HTML for the figure
    user_pie_html = plot(fig, output_type='div')

    return user_pie_html

def update_seller_bar():
    # Dummy data for sellers
    sellers = [{'store_name': 'Store A'}, {'store_name': 'Store B'}, {'store_name': 'Store C'}]
    seller_count = len(sellers)

    # Create data trace for the bar chart
    data = [
        go.Bar(
            x=[seller['store_name'] for seller in sellers],  # x-axis: store names
            y=[seller_count] * seller_count  # y-axis: seller count repeated for each seller
        )
    ]

    # Define layout for the bar chart
    layout = go.Layout(title='Seller Count')

    # Create figure
    fig = go.Figure(data=data, layout=layout)

    # Generate HTML for the figure
    seller_bar_html = plot(fig, output_type='div')

    return seller_bar_html


def Dashboard(request, *args, **kwargs):
        # Update each graph
        user_pie_html = update_user_pie()
        seller_bar_html = update_seller_bar()

        # Render the HTML template with the graph HTML content
        return render(request, 'storefront/plotly-graphs.html', { 'user_pie_html': user_pie_html, 'seller_bar_html': seller_bar_html})
    








# Create your views here.
