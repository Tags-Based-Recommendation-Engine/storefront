from django.shortcuts import render, redirect
from django.contrib.auth import login, logout , authenticate
from django.contrib.auth.decorators import login_required
from storefront.models import Product, Category, Listing, Product_Images
from .models import Review, CartItem, Interaction
from django.db.models import Q
import numpy as np
import random
from tensorflow.keras.models import load_model
from webstore.settings import MODEL_PATH
from django.db.models.functions import Random
from django.db.models import Min
from functools import reduce
import operator

model = load_model(MODEL_PATH)

def get_optimized_price(inventory, min_price, max_price, rating, strategy, user_interest):
    input_data = np.array([[int(inventory), int(min_price), int(max_price), int(rating), strategy]])
    discount = model.predict(input_data)[0][0]
    if user_interest==0:
        discount += (0.15*discount)
    else:
        discount -= (0.15*discount*(user_interest))
    predicted_price = max_price-int(discount)
    optimized_price = int(min(max(predicted_price,min_price),max_price))
    return optimized_price

def search(request, query):
    # Split the query into individual words
    search_terms = query.split()

    # Initialize an empty queryset to store the results
    results = Product.objects.none()
    listings = Listing.objects.none()
    
    # Iterate over each word in the search query and filter the Listing queryset
    for term in search_terms:
        # Filter listings by matching name field
        listing_matches = Product.objects.filter(
            Q(product_name__icontains=term)
        )
        # Add the matching listings to the results queryset
        results |= listing_matches

    for result in results:
        listing_matches = Listing.objects.filter(product=result)
        # Order the listings by min_price and select the one with the lowest price
        min_price_listing = listing_matches.order_by('current_price')[:3]
        Interaction.objects.create(
            User=request.user,
            listing=min_price_listing.first(),
            action='search'
        )
        if min_price_listing:
            listings |= min_price_listing

    # Return the final queryset containing all matching listings
    context = {
        'product': listings.distinct(),
        'query'  : query,
    }

    
    # Return the final queryset containing all matching products
    return render(request, 'market/search.html', context)

def index(request):
    products = Product.objects.all()
    listings = Listing.objects.order_by(Random())[:30]
    categories = Category.objects.all()
    
    if request.method == 'POST':
        search_text = request.POST.get('searchtext')
        return redirect('search', query=search_text)  # Redirect to the search view with the search query
    
    if request.user:
        user_interest = 1
    else:
        user_interest = 0

    for listing in listings:
        optimized_price = get_optimized_price(listing.inventory, listing.min_price, listing.max_price, listing.rating, listing.strategy, user_interest)
        setattr(listing, 'optimized_price', optimized_price)  

    context = {
        'product': products,
        'catagory': categories,
        'listings': listings
    }
    
    return render(request, 'market/index.html', context)

@login_required
def cart(request):
    cartitems = CartItem.objects.filter(customer=request.user)
    
    # Calculate the total price of all items in the cart
    subtotal = sum(item.product.current_price for item in cartitems)
    total = sum(item.product.current_price for item in cartitems)+10

    context = {
        'cartitems': cartitems,
        'total': total,
        'subtotal': subtotal
    }

    return render(request, 'market/cart.html', context)

@login_required
def product(request, slug):
    product = Listing.objects.get(slug=slug)
    prod = product.product
    imgs = Product_Images.objects.filter(product=prod)

    Interaction.objects.create(
        User=request.user,
        listing=product,
        action='clicked'
    )

    reviews = Review.objects.filter(listing=product)
    listings =  Listing.objects.exclude(id=product.id).order_by('?')[:4]
    
    if request.method == 'POST':
        CartItem.objects.create(
            customer = request.user,
            product = product

        )
        Interaction.objects.create(
            User=request.user,
            listing=product,
            action='Added to cart'
        )
        return redirect('cart')
           # Get 4 random related
    context = {
        'product':product,
        'reviews':reviews,
        'listings':listings,
        'imgs': imgs
    }
    return render(request, 'market/product.html', context)


@login_required
def empty_cart(request):
    CartItem.objects.filter(customer=request.user).delete()
    return redirect('cart')

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('index')