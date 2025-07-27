from store.models import Book

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, book):
        book_id = str(book.id)
        if book_id not in self.cart:
            self.cart[book_id] = {'quantity': 1}
        else:
            # Ensure 'quantity' key exists before incrementing
            self.cart[book_id]['quantity'] = self.cart[book_id].get('quantity', 1) + 1
        self.save()

    def remove(self, book):
        book_id = str(book.id)
        if book_id in self.cart:
            del self.cart[book_id]
            self.save()

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True
    def decrement(self, book):
        book_id = str(book.id)
        if book_id in self.cart:
            if self.cart[book_id]['quantity'] > 1:
                self.cart[book_id]['quantity'] -= 1
            else:
                del self.cart[book_id]
            self.save()


    def get_items(self):
        book_ids = self.cart.keys()
        books = Book.objects.filter(id__in=book_ids)
        items = []

        for book in books:
            book_id = str(book.id)
            quantity = self.cart[book_id].get('quantity', 1)  # 🛠️ Safe access
            items.append({
                'book': book,
                'quantity': quantity,
                'total_price': book.price * quantity
            })
        return items

    def get_total(self):
        return sum(item['total_price'] for item in self.get_items())
