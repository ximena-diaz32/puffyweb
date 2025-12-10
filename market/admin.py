from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'stock', 'descripcion', 'imagen']  # Campos visibles en la lista
    list_editable = ['precio', 'stock']  # Campos editables directamente desde la lista
    search_fields = ['nombre', 'descripcion']  # Búsqueda por nombre o descripción
    list_per_page = 20  # Opcional: paginación

    # Redirige después de agregar un producto
    def response_add(self, request, obj, post_url_continue=None):
        return HttpResponseRedirect(reverse('market_index'))

    # Redirige después de editar un producto
    def response_change(self, request, obj):
        return HttpResponseRedirect(reverse('market_index'))