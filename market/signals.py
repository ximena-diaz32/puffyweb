from django.contrib.auth.signals import user_logged_out, user_logged_in
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.apps import apps
from django.db.utils import OperationalError, ProgrammingError

from .models import CarritoGuardado

@receiver(user_logged_out)
def guardar_carrito_al_cerrar_sesion(sender, request, user, **kwargs):
    if user.is_authenticated:
        carrito = request.session.get('cart', {})
        if carrito:
            try:
                CarritoGuardado.objects.update_or_create(
                    usuario=user,
                    defaults={'datos': carrito}
                )
            except (OperationalError, ProgrammingError):
                # La tabla aún no existe (por ejemplo, antes de migrar)
                pass

@receiver(user_logged_in)
def restaurar_carrito_al_iniciar_sesion(sender, request, user, **kwargs):
    try:
        guardado = CarritoGuardado.objects.get(usuario=user)
        request.session['cart'] = guardado.datos
    except (CarritoGuardado.DoesNotExist, OperationalError, ProgrammingError):
        pass