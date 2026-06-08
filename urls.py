from django.urls import path
from . import views

urlpatterns = [

    path('', views.home),

    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('register/', views.register),

    path('product/<int:id>/', views.product_detail),

    path('add-to-cart/<int:id>/', views.add_to_cart),

    path('cart/', views.cart),

    path('remove-from-cart/<int:id>/', views.remove_from_cart),
    path('order/',views.place_order),
    path('orders/',views.orders),
    path('buy-now/<int:id>/', views.buy_now),
    path('checkout/', views.checkout),
    path('wishlist/', views.wishlist),
path('add-to-wishlist/<int:id>/', views.add_to_wishlist),
path('profile/', views.profile),
]