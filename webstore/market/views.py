from django.shortcuts import render, redirect
from django.contrib.auth import login, logout , authenticate
from django.contrib.auth.decorators import login_required
from storefront.models import Product, Category, Listing, Product_Images
from .models import Review, CartItem
from django.db.models import Q


def search(request, query):
    # Split the query into individual words
    search_terms = query.split()

    # Initialize an empty queryset to store the results
    results = Listing.objects.none()

    # Iterate over each word in the search query and filter the Listing queryset
    for term in search_terms:
        # Filter listings by matching name field
        listing_matches = Listing.objects.filter(
            Q(name__icontains=term)
        )
        # Add the matching listings to the results queryset
        results |= listing_matches

    # Return the final queryset containing all matching listings
    context = {
        'product': results.distinct(),
        'query'  : query,
    }

    # Return the final queryset containing all matching products
    return render(request, 'market/search.html', context)

def index(request):
    products = Product.objects.all()
    listing = Listing.objects.all()
    categories = Category.objects.all()

    if request.method == 'POST':
        search_text = request.POST.get('searchtext')
        return redirect('search', query=search_text)  # Redirect to the search view with the search query

    context = {
        'product': products,
        'catagory': categories,
        'listings': listing
    }
    return render(request, 'market/index.html', context)

@login_required
def cart(request):
    cartitems = CartItem.objects.filter(customer=request.user)
    
    # Calculate the total price of all items in the cart
    subtotal = sum(item.product.current_price for item in cartitems)
    total = sum(item.product.current_price for item in cartitems)+1000
    
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

    reviews = Review.objects.filter(listing=product)
    listings =  Listing.objects.exclude(id=product.id).order_by('?')[:4]
    
    if request.method == 'POST':
        CartItem.objects.create(
            customer = request.user,
            product = product

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