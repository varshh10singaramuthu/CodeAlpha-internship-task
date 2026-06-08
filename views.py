from django.shortcuts import render, get_object_or_404, redirect
from .models import Product

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# HOME PAGE
@login_required(login_url='/login/')
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


# PRODUCT DETAIL PAGE
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})


# ADD TO CART
def add_to_cart(request, id):
    cart = request.session.get('cart', [])

    cart.append(id)

    request.session['cart'] = cart

    return redirect('/')


# CART PAGE
def cart(request):
    cart_items = request.session.get('cart', [])

    products = Product.objects.filter(id__in=cart_items)

    total = sum(product.price for product in products)

    return render(request, 'cart.html', {
        'products': products,
        'total': total
    })


# REMOVE FROM CART
def remove_from_cart(request, id):
    cart_items = request.session.get('cart', [])

    if id in cart_items:
        cart_items.remove(id)

    request.session['cart'] = cart_items

    return redirect('/cart/')


# REGISTER
def register(request):

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST.get('email')

        password = request.POST['password']

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('/login/')

    return render(request, 'register.html')


# LOGIN
def login_view(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('/')

    return render(request, 'login.html')


# LOGOUT
def logout_view(request):

    logout(request)

    return redirect('/login/')
from .models import Order

@login_required(login_url='/login/')
def place_order(request):
    cart = request.session.get('cart', [])

    for product_id in cart:
        product = Product.objects.get(id=product_id)
        Order.objects.create(
            user=request.user,
            product=product
        )

    request.session['cart'] = []

    return render(request, 'success.html')
@login_required(login_url='/login/')
def orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders.html', {'orders': orders})
@login_required(login_url='/login/')
def buy_now(request, id):
    request.session['cart'] = [id]
    return redirect('/checkout/')
@login_required(login_url='/login/')
def checkout(request):
    cart = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart)

    return render(request, 'checkout.html', {'products': products})
@login_required(login_url='/login/')
def add_to_wishlist(request, id):
    wishlist = request.session.get('wishlist', [])

    if id not in wishlist:
        wishlist.append(id)

    request.session['wishlist'] = wishlist

    return redirect('/wishlist/')
@login_required(login_url='/login/')
def wishlist(request):
    wishlist = request.session.get('wishlist', [])
    products = Product.objects.filter(id__in=wishlist)

    return render(request, 'wishlist.html', {'products': products})
@login_required(login_url='/login/')
def profile(request):
    orders = Order.objects.filter(user=request.user)
    total_orders = orders.count()

    return render(request, 'profile.html', {
        'total_orders': total_orders
    })
@login_required(login_url='/login/')
def profile(request):

    # Orders
    orders = Order.objects.filter(user=request.user)

    # Total Orders
    total_orders = orders.count()

    # Total Amount Spent
    total_amount = sum(order.product.price for order in orders)

    # Wishlist Count
    wishlist = request.session.get('wishlist', [])
    wishlist_count = len(wishlist)

    # Recent Orders (last 3)
    recent_orders = orders.order_by('-order_date')[:3]

    return render(request, 'profile.html', {
        'total_orders': total_orders,
        'total_amount': total_amount,
        'wishlist_count': wishlist_count,
        'recent_orders': recent_orders
    })