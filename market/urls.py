from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Página principal y navegación general
    path('', views.inicio, name='inicio'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('contacto/', views.contacto, name='contacto'),

    # Panel de administración de productos
    path('panel/', views.index, name='market'),  # ← Cambié 'market/' por 'panel/' para evitar ambigüedad
    path('panel/crear/', views.crear, name='crear'),
    path('panel/editar/<int:id>/', views.editar, name='editar'),
    path('panel/eliminar/<int:id>/', views.eliminar, name='eliminar'),

    # Página pública de productos
    path('listado/', views.listado, name='listado'),

    # Carrito de compras
    path('carro/', views.ver_carro, name='ver_carro'),
    path('carro/agregar/<int:id>/', views.agregar_al_carro, name='agregar_al_carro'),
    path('carro/actualizar/<int:id>/', views.actualizar_carro, name='actualizar_carro'),
    path('carro/vaciar/', views.vaciar_carro, name='vaciar_carro'),

    # Autenticación de usuarios
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='inicio'), name='logout'),
    path('accounts/registro/', views.registro, name='registro'),
    path('accounts/perfil/', views.perfil, name='perfil'),
    # Checkout
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/invitado/', views.checkout_invitado, name='checkout_invitado'),
    path('politicas-privacidad/', views.politicas_privacidad, name='politicas_privacidad'),
    path('politicas-envio/', views.politicas_envio, name='politicas_envio'),
]