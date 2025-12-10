# market/context_processors.py

from .cart import Cart

def carrito_total(request):
    cart = Cart(request)
    return {
        'carrito_total': cart.total_items()
    }