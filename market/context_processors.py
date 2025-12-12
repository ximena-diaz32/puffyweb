# market/context_processors.py

from .cart import Cart

def carrito_total(request):
    cart = Cart(request)
    return {
        'carrito_total': cart.total_items()
    }

from .cart import Cart

def carrito_total(request):
    cart = Cart(request)

    for item in cart.cart.values():
        try:
            item['subtotal'] = float(item['precio']) * int(item['cantidad'])
        except (ValueError, TypeError):
            item['subtotal'] = 0

    return {
        'carro': cart.cart,
        'carrito_total': cart.total_items()
    }