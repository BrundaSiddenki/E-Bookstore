from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages

from .models import Book, Order, OrderItem, WishlistItem
from .forms import CheckoutForm
from .cart import Cart

# 🏠 Home Page – Displays All Books
def home(request):
    query = request.GET.get('q', '')
    books = Book.objects.filter(
        Q(title__icontains=query) | Q(author__icontains=query)
    ) if query else Book.objects.all()
    return render(request, 'store/home.html', {'books': books})

# ➕ Add to Cart
def add_to_cart(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    cart.add(book)
    return redirect('view_cart')

# ➖ Remove from Cart
def remove_from_cart(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    cart.remove(book)
    return redirect('view_cart')

# 🔼 Increment Cart Quantity
@login_required
def increment_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart = Cart(request)
    cart.add(book)
    return redirect('view_cart')

# 🔽 Decrement Cart Quantity
@login_required
def decrement_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart = Cart(request)
    cart.decrement(book)
    return redirect('view_cart')

# 🛒 View Cart
def view_cart(request):
    cart = Cart(request)
    context = {
        'cart_items': cart.get_items(),
        'total': cart.get_total(),
    }
    return render(request, 'store/cart.html', context)

# 🔍 Search Books
def search_books(request):
    query = request.GET.get('q', '')
    results = Book.objects.filter(
        Q(title__icontains=query) | Q(author__icontains=query)
    ) if query else []
    return render(request, 'store/search_results.html', {
        'query': query,
        'results': results
    })

# 🧾 Checkout Page
@login_required
def checkout(request):
    cart = Cart(request)
    cart_items = cart.get_items()

    if not cart_items:
        return redirect('view_cart')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                full_name=form.cleaned_data['full_name'],
                address=form.cleaned_data['address'],
                phone=form.cleaned_data['phone'],
            )
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    book=item['book'],
                    quantity=item['quantity'],
                )
            cart.cart.clear()
            cart.save()
            return render(request, 'store/thank_you.html', {'order': order})
    else:
        form = CheckoutForm()

    return render(request, 'store/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total': cart.get_total(),
    })

# 💖 View Wishlist
@login_required
def view_wishlist(request):
    wishlist_items = WishlistItem.objects.filter(user=request.user)
    return render(request, 'store/wishlist.html', {'wishlist_items': wishlist_items})

# ➕ Add to Wishlist
@login_required
def add_to_wishlist(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    WishlistItem.objects.get_or_create(user=request.user, book=book)
    messages.success(request, f"✅ '{book.title}' added to your wishlist.")
    return redirect('home')

# ❌ Remove from Wishlist
@login_required
def remove_from_wishlist(request, book_id):
    WishlistItem.objects.filter(user=request.user, book_id=book_id).delete()
    messages.success(request, "❌ Removed book from wishlist.")
    return redirect('view_wishlist')

# 📦 Order History
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})
from django.contrib import messages
from .models import Book, WishlistItem

@login_required
def add_to_wishlist(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    WishlistItem.objects.get_or_create(user=request.user, book=book)
    messages.success(request, f"'{book.title}' added to wishlist!")
    return redirect('home')

@login_required
def view_wishlist(request):
    wishlist_items = WishlistItem.objects.filter(user=request.user)
    return render(request, 'store/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def remove_from_wishlist(request, book_id):
    WishlistItem.objects.filter(user=request.user, book_id=book_id).delete()
    messages.success(request, "Book removed from wishlist.")
    return redirect('wishlist')