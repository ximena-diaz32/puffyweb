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

        if disponible <= 0:
            return  # No hay stock disponible

        cantidad_a_agregar = min(cantidad, disponible)

        if producto_id not in self.cart:
            self.cart[producto_id] = {
                'nombre': producto.nombre,
                'precio': str(producto.precio),
                'cantidad': cantidad_a_agregar
            }
        else:
            self.cart[producto_id]['cantidad'] += cantidad_a_agregar

        self.save()

    def update(self, producto, cantidad):
        producto_id = str(producto.id)
        if cantidad <= 0:
            self.remove(producto)
        else:
            if cantidad > producto.stock:
                cantidad = producto.stock
            if producto_id in self.cart:
                self.cart[producto_id]['cantidad'] = cantidad
            else:
                self.cart[producto_id] = {
                    'nombre': producto.nombre,
                    'precio': str(producto.precio),
                    'cantidad': cantidad
                }
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
        total = 0
        for item in self.cart.values():
            total += float(item['precio']) * int(item['cantidad'])
        return total