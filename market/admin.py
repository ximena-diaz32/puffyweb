from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse

from .models import Producto, Pedido, DetallePedido, CarritoGuardado, Perfil

# Mostrar Perfil como inline dentro del admin de User
class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfil'
    fk_name = 'usuario'

class UserAdmin(BaseUserAdmin):
    inlines = (PerfilInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Inline para mostrar los detalles del pedido dentro del admin de Pedido
class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    can_delete = False
    readonly_fields = ('producto', 'cantidad', 'precio_entero')
    fields = ('producto', 'cantidad', 'precio_entero')

    def precio_entero(self, obj):
        return f"${int(obj.precio)}" if obj.precio is not None else "-"
    precio_entero.short_description = 'Precio'

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_entero', 'stock')

    def precio_entero(self, obj):
        return f"${int(obj.precio)}" if obj.precio is not None else "-"
    precio_entero.short_description = 'Precio (CLP)'

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'comprador', 'fecha', 'estado')
    list_editable = ('estado',)
    list_filter = ('fecha', 'estado')
    search_fields = ('usuario__username', 'nombre', 'email', 'id')
    inlines = [DetallePedidoInline]

    readonly_fields = ('usuario', 'mostrar_nombre', 'mostrar_email', 'mostrar_direccion', 'mostrar_telefono', 'fecha')

    fieldsets = (
        (None, {
            'fields': ('usuario', 'fecha', 'estado')
        }),
        ('Datos del comprador', {
            'fields': ('mostrar_nombre', 'mostrar_email', 'mostrar_direccion', 'mostrar_telefono')
        }),
    )

    def comprador(self, obj):
        if obj.usuario:
            return f"{obj.usuario.username} ({obj.usuario.email})"
        return f"{obj.nombre or 'Invitado'} ({obj.email or 'sin email'})"
    comprador.short_description = 'Comprador'

    def mostrar_nombre(self, obj):
        return obj.usuario.username if obj.usuario else obj.nombre
    mostrar_nombre.short_description = 'Nombre'

    def mostrar_email(self, obj):
        return obj.usuario.email if obj.usuario else obj.email
    mostrar_email.short_description = 'Email'

    def mostrar_direccion(self, obj):
        if obj.usuario and hasattr(obj.usuario, 'perfil'):
            return obj.usuario.perfil.direccion
        return obj.direccion
    mostrar_direccion.short_description = 'Dirección'

    def mostrar_telefono(self, obj):
        if obj.usuario and hasattr(obj.usuario, 'perfil'):
            return obj.usuario.perfil.telefono
        return obj.telefono
    mostrar_telefono.short_description = 'Teléfono'

@admin.register(CarritoGuardado)
class CarritoGuardadoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'actualizado')