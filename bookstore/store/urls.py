from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-to-cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:book_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('wishlist/', views.view_wishlist, name='wishlist'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_history, name='order_history'),
    path('search/', views.search_books, name='search_books'),
    path('wishlist/add/<int:book_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:book_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/add/<int:book_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    # store/urls.py
    path('checkout/', views.checkout, name='checkout'),
    path('cart/increment/<int:book_id>/', views.increment_cart, name='increment_cart'),
    path('cart/decrement/<int:book_id>/', views.decrement_cart, name='decrement_cart'),

]

