from decimal import Decimal

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, producto, cantidad=1):
        producto_id = str(producto.id)
        cantidad_en_carrito = self.cart.get(producto_id, {}).get('cantidad', 0)
        disponible = producto.stock - cantidad_en_carrito

        if producto.tipo == 'digital':
            # Solo permitir uno, sin importar la cantidad solicitada
            if producto_id in self.cart:
                return  # Ya está en el carrito
            self.cart[producto_id] = {
                'nombre': producto.nombre,
                'precio': str(producto.precio),
                'cantidad': 1,
                'tipo': producto.tipo,
                'subtotal': str(producto.precio)
            }
        else:
            if disponible <= 0:
                return  # No hay stock disponible

            cantidad_a_agregar = min(cantidad, disponible)

            if producto_id not in self.cart:
                self.cart[producto_id] = {
                    'nombre': producto.nombre,
                    'precio': str(producto.precio),
                    'cantidad': cantidad_a_agregar,
                    'tipo': producto.tipo
                }
            else:
                self.cart[producto_id]['cantidad'] += cantidad_a_agregar

            subtotal = Decimal(self.cart[producto_id]['precio']) * self.cart[producto_id]['cantidad']
            self.cart[producto_id]['subtotal'] = str(subtotal)

        self.save()

    def update(self, producto, cantidad):
        producto_id = str(producto.id)

        if producto.tipo == 'digital':
            # No permitir cambiar cantidad de productos digitales
            return

        if cantidad <= 0:
            self.remove(producto)
        else:
            cantidad = min(cantidad, producto.stock)
            if producto_id in self.cart:
                self.cart[producto_id]['cantidad'] = cantidad
            else:
                self.cart[producto_id] = {
                    'nombre': producto.nombre,
                    'precio': str(producto.precio),
                    'cantidad': cantidad,
                    'tipo': producto.tipo
                }
            subtotal = Decimal(self.cart[producto_id]['precio']) * cantidad
            self.cart[producto_id]['subtotal'] = str(subtotal)

        self.save()

    def remove(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.cart:
            del self.cart[producto_id]
            self.save()

    def clear(self):
        self.session['cart'] = {}
        self.save()

    def save(self):
        self.session.modified = True

    def items(self):
        return self.cart.items()

    def total_items(self):
        return sum(item['cantidad'] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            Decimal(item['precio']) * item['cantidad']
            for item in self.cart.values()
        )