from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Pedido, DetallePedido, CarritoGuardado, Perfil
from .forms import ProductoForm, CheckoutInvitadoForm, RegistroForm
from .cart import Cart
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login


# Panel de administración
def index(request):
    productos = Producto.objects.all()
    return render(request, 'market/index.html', {'market': productos})

def crear(request):
    if request.method == 'POST':
        formulario = ProductoForm(request.POST, request.FILES)
        if formulario.is_valid():
            producto = formulario.save(commit=False)
            producto.save()
            if 'imagen' in request.FILES:
                producto.imagen = request.FILES['imagen']
                producto.save()
            return redirect('market')
    else:
        formulario = ProductoForm()
    return render(request, 'market/form.html', {'formulario': formulario})

def editar(request, id):
    producto = get_object_or_404(Producto, pk=id)
    if request.method == 'POST':
        formulario = ProductoForm(request.POST, request.FILES, instance=producto)
        if formulario.is_valid():
            formulario.save()
            return redirect('market')
    else:
        formulario = ProductoForm(instance=producto)
    return render(request, 'market/form.html', {'formulario': formulario})

def eliminar(request, id):
    producto = get_object_or_404(Producto, pk=id)
    producto.delete()
    return redirect('market')

def eliminar_del_carro(request, id):
    producto = get_object_or_404(Producto, id=id)
    cart = Cart(request)
    cart.remove(producto)
    return redirect('ver_carro')

# Público
def listado(request):
    productos = Producto.objects.all()
    cart = Cart(request)
    cantidades = {int(pid): item['cantidad'] for pid, item in cart.cart.items()}

    # Calcular disponibilidad
    for producto in productos:
        producto.disponible = max(producto.stock - cantidades.get(producto.id, 0), 0)

    # Detectar patrones digitales ya en el carrito
    digitales_en_carro = [
        int(pid) for pid in cart.cart.keys()
        if Producto.objects.filter(id=pid, tipo='digital').exists()
    ]

    return render(request, 'market/listado.html', {
        'productos': productos,
        'digitales_en_carro': digitales_en_carro,
    })

def nosotros(request):
    return render(request, 'paginas/nosotros.html')

def inicio(request):
    return render(request, 'paginas/inicio.html')

def contacto(request):
    return render(request, 'paginas/contacto.html')

# Carrito
@require_POST
def agregar_al_carro(request, id):
    producto = get_object_or_404(Producto, id=id)
    cart = Cart(request)
    cantidad_en_carrito = cart.cart.get(str(producto.id), {}).get('cantidad', 0)

    # Si es digital, solo permitir agregar una vez
    if producto.tipo == 'digital':
        if cantidad_en_carrito >= 1:
            # Ya está en el carrito, no agregar de nuevo
            return redirect('listado')
        else:
            cart.add(producto, 1)
            return redirect('listado')

    # Producto físico: respetar stock
    cantidad = int(request.POST.get('cantidad', 1))
    disponible = producto.stock - cantidad_en_carrito
    if disponible <= 0:
        return redirect('listado')

    cantidad_a_agregar = min(cantidad, disponible)
    cart.add(producto, cantidad_a_agregar)
    return redirect('listado')

def vaciar_carro(request):
    cart = Cart(request)
    cart.clear()
    return redirect('ver_carro')

def actualizar_carro(request, id):
    producto = get_object_or_404(Producto, id=id)
    cart = Cart(request)

    # No permitir actualizar productos digitales
    if producto.tipo == 'digital':
        return redirect('ver_carro')

    if request.method == 'POST':
        try:
            cantidad = int(request.POST.get('cantidad', 1))
        except (TypeError, ValueError):
            cantidad = 1

        cart.update(producto, cantidad)

    return redirect('ver_carro')


    if request.method == 'POST':
        try:
            cantidad = int(request.POST.get('cantidad', 1))
            if cantidad < 1:
                cantidad = 1
        except (ValueError, TypeError):
            cantidad = 1

        cart.update(producto, cantidad)

    return redirect('ver_carro')

def ver_carro(request):
    cart = Cart(request)
    return render(request, 'market/carro.html', {
        'carro': cart.cart,
        'carro_total': cart.get_total_price()
    })


# Registro y perfil
def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tu cuenta ha sido creada con éxito! Ahora puedes iniciar sesión.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})

def perfil(request):
    if not request.user.is_authenticated:
        return redirect('login')
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'registration/perfil.html', {'pedidos': pedidos})

# Checkout autenticado
@login_required
def checkout(request):
    cart = Cart(request)
    if not cart.cart:
        return redirect('ver_carro')

    pedido = Pedido.objects.create(usuario=request.user)

    for producto_id, item in cart.cart.items():
        try:
            producto = Producto.objects.get(id=producto_id)
            cantidad = item['cantidad']

            if producto.stock >= cantidad:
                DetallePedido.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=cantidad,
                    precio=producto.precio  # ← precio congelado al momento de la compra
                )
                producto.stock -= cantidad
                producto.save()
            else:
                return render(request, 'carro.html', {
                    'error': f"No hay suficiente stock para {producto.nombre}."
                })

        except Producto.DoesNotExist:
            continue

    cart.clear()
    CarritoGuardado.objects.filter(usuario=request.user).delete()
    return redirect('seleccion_pago')

# Checkout invitado
@csrf_exempt
def checkout_invitado(request):
    if request.method == 'POST':
        form = CheckoutInvitadoForm(request.POST)
        if form.is_valid():
            # Guardamos los datos del formulario en la sesión
            request.session['checkout_invitado'] = form.cleaned_data
            return redirect('seleccion_pago')
    else:
        form = CheckoutInvitadoForm()

    return render(request, 'market/checkout_invitado.html', {'form': form})


# Selección de método de pago
@csrf_exempt
def seleccion_pago(request):
    return render(request, 'market/seleccion_pago.html')

# Confirmación de pedido
@csrf_exempt
def checkout_confirmacion(request):
    if request.method != 'POST':
        return redirect('seleccion_pago')

    metodo = request.POST.get('metodo_pago', 'desconocido')
    cart = Cart(request)

    if request.user.is_authenticated:
        if not cart.cart:
            return redirect('ver_carro')

        pedido = Pedido.objects.create(usuario=request.user)

        for producto_id, item in cart.cart.items():
            try:
                producto = Producto.objects.get(id=producto_id)
                cantidad = item['cantidad']

                if producto.stock >= cantidad:
                    DetallePedido.objects.create(
                        pedido=pedido,
                        producto=producto,
                        cantidad=cantidad
                    )
                    producto.stock -= cantidad
                    producto.save()
                else:
                    return render(request, 'market/carro.html', {
                        'carro': cart.cart,
                        'carro_total': cart.get_total_price(),
                        'error': f"No hay suficiente stock para {producto.nombre}."
                    })

            except Producto.DoesNotExist:
                continue

        #  Obtener productos digitales del pedido
        productos_digitales = DetallePedido.objects.filter(
            pedido=pedido,
            producto__tipo='digital'
        ).select_related('producto')

        #  Limpiar carrito y carrito guardado
        cart.clear()
        CarritoGuardado.objects.filter(usuario=request.user).delete()

        #  Renderizar confirmación con productos digitales
        return render(request, 'market/checkout_confirmacion.html', {
            'metodo': metodo,
            'pedido': pedido,
            'productos_digitales': productos_digitales,
        })
    else:
        return redirect('market/listado.html')
# Políticas
def politicas_privacidad(request):
    return render(request, 'paginas/politicas_privacidad.html')

def politicas_envio(request):
    return render(request, 'paginas/politicas_envio.html')

@csrf_exempt
def checkout_confirmacion_invitado(request):
    if request.method != 'POST':
        return redirect('seleccion_pago')

    metodo = request.POST.get('metodo_pago', 'desconocido')
    cart = Cart(request)

    if not cart.cart:
        return redirect('ver_carro')

    # Obtener datos del formulario guardados en sesión
    datos = request.session.get('checkout_invitado', {})

    # Crear el pedido con los datos del comprador invitado
    pedido = Pedido.objects.create(
        usuario=None,
        nombre=datos.get('nombre'),
        email=datos.get('email'),
        direccion=datos.get('direccion'),
        telefono=datos.get('telefono')
    )

    for producto_id, item in cart.cart.items():
        try:
            producto = Producto.objects.get(id=producto_id)
            cantidad = item['cantidad']

            if producto.stock >= cantidad:
                DetallePedido.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=cantidad,
                    precio=producto.precio  # ← precio congelado al momento de la compra
                )
                producto.stock -= cantidad
                producto.save()
            else:
                return render(request, 'market/carro.html', {
                    'carro': cart.cart,
                    'carro_total': cart.get_total_price(),
                    'error': f"No hay suficiente stock para {producto.nombre}."
                })

        except Producto.DoesNotExist:
            continue

    productos_digitales = DetallePedido.objects.filter(
        pedido=pedido,
        producto__tipo='digital'
    ).select_related('producto')

    cart.clear()
    request.session.pop('checkout_invitado', None)  # Limpia los datos de sesión

    return render(request, 'market/checkout_confirmacion.html', {
        'metodo': metodo,
        'pedido': pedido,
        'productos_digitales': productos_digitales,
    })


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.email = form.cleaned_data['email']
            user.save()

            Perfil.objects.create(
                usuario=user,
                direccion=form.cleaned_data['direccion'],
                telefono=form.cleaned_data['telefono']
            )

            login(request, user)
            return redirect('inicio')  # ← corregido aquí
    else:
        form = RegistroForm()

    return render(request, 'registration/registro.html', {'form': form})