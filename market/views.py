from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Pedido
from .forms import ProductoForm
from .cart import Cart
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Producto, Pedido, DetallePedido, CarritoGuardado



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

# Público
def listado(request):
    productos = Producto.objects.all()
    cart = Cart(request)
    cantidades = {int(pid): item['cantidad'] for pid, item in cart.cart.items()}
    for producto in productos:
        producto.disponible = max(producto.stock - cantidades.get(producto.id, 0), 0)
    return render(request, 'market/listado.html', {'productos': productos})

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
    cantidad = int(request.POST.get('cantidad', 1))
    cart = Cart(request)
    cantidad_en_carrito = cart.cart.get(str(producto.id), {}).get('cantidad', 0)
    disponible = producto.stock - cantidad_en_carrito
    if disponible <= 0:
        return redirect('listado')
    cantidad_a_agregar = min(cantidad, disponible)
    cart.add(producto, cantidad_a_agregar)
    return redirect('listado')

def ver_carro(request):
    cart = Cart(request)
    return render(request, 'market/carro.html', {
        'carro': cart.cart,
        'carro_total': cart.get_total_price()
    })

def vaciar_carro(request):
    cart = Cart(request)
    cart.clear()
    return redirect('ver_carro')

@require_POST
def actualizar_carro(request, id):
    producto = get_object_or_404(Producto, id=id)
    cantidad = int(request.POST.get('cantidad', 1))
    cart = Cart(request)
    cart.update(producto, cantidad)
    return redirect('ver_carro')

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
                    cantidad=cantidad
                )
                producto.stock -= cantidad
                producto.save()
            else:
                return render(request, 'carro.html', {
                    'error': f"No hay suficiente stock para {producto.nombre}."
                })

        except Producto.DoesNotExist:
            continue

    # Vaciar carrito de sesión
    cart.clear()

    # Eliminar carrito guardado en base de datos
    CarritoGuardado.objects.filter(usuario=request.user).delete()

    # Redirigir al servicio de pago externo
    return redirect('https://www.tuserviciodepago.com/pagar')

# Checkout invitado
@csrf_exempt
def checkout_invitado(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        direccion = request.POST.get('direccion')
        # Aquí podrías guardar los datos en sesión o en un modelo temporal
        return redirect('https://www.tuserviciodepago.com/pagar')
        return render(request, 'market/checkout_invitado.html')

def politicas_privacidad(request):
    return render(request, 'paginas/politicas_privacidad.html')

def politicas_envio(request):
    return render(request, 'paginas/politicas_envio.html')