import os
from django.db.models.signals import post_delete, pre_save
from django.contrib.auth.signals import user_logged_out, user_logged_in
from django.dispatch import receiver
from django.db.utils import OperationalError, ProgrammingError
from .models import CarritoGuardado, Producto

# Guardar carrito al cerrar sesión
@receiver(user_logged_out)
def guardar_carrito_al_cerrar_sesion(sender, request, user, **kwargs):
    try:
        if user and user.is_authenticated:
            carrito = request.session.get('cart', {})
            if carrito:
                CarritoGuardado.objects.update_or_create(
                    usuario=user,
                    defaults={'datos': carrito}
                )
    except Exception as e:
        print(f"Error al guardar carrito al cerrar sesión: {e}")

# Restaurar carrito al iniciar sesión
@receiver(user_logged_in)
def restaurar_carrito_al_iniciar_sesion(sender, request, user, **kwargs):
    try:
        guardado = CarritoGuardado.objects.get(usuario=user)
        request.session['cart'] = guardado.datos
    except (CarritoGuardado.DoesNotExist, OperationalError, ProgrammingError):
        pass

# Eliminar archivos al eliminar producto
@receiver(post_delete, sender=Producto)
def eliminar_archivos_producto(sender, instance, **kwargs):
    for campo in ['imagen', 'archivo']:
        archivo = getattr(instance, campo)
        if archivo and hasattr(archivo, 'path') and os.path.isfile(archivo.path):
            try:
                os.remove(archivo.path)
            except Exception as e:
                print(f"No se pudo eliminar {campo}: {e}")

# Eliminar archivos antiguos al reemplazar imagen o archivo digital
@receiver(pre_save, sender=Producto)
def reemplazar_archivos_anteriores(sender, instance, **kwargs):
    try:
        producto_anterior = Producto.objects.get(pk=instance.pk)
    except Producto.DoesNotExist:
        return  # Es un producto nuevo

    for campo in ['imagen', 'archivo']:
        archivo_anterior = getattr(producto_anterior, campo)
        archivo_nuevo = getattr(instance, campo)

        if archivo_anterior and archivo_anterior != archivo_nuevo:
            if hasattr(archivo_anterior, 'path') and os.path.isfile(archivo_anterior.path):
                try:
                    os.remove(archivo_anterior.path)
                except Exception as e:
                    print(f"No se pudo eliminar {campo} anterior: {e}")