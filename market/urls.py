from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Página principal y navegación general
    path('', views.inicio, name='inicio'),  # ← nombre corregido aquí
    path('nosotros/', views.nosotros, name='nosotros'),
    path('contacto/', views.contacto, name='contacto'),

    # Panel de administración de productos
    path('panel/', views.index, name='market'),
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
    path('carro/eliminar/<int:id>/', views.eliminar_del_carro, name='eliminar_del_carro'),


    # Autenticación de usuarios
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='inicio'), name='logout'),
    path('accounts/registro/', views.registro, name='registro'),
    path('accounts/perfil/', views.perfil, name='perfil'),

    # Checkout
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/invitado/', views.checkout_invitado, name='checkout_invitado'),
    path('checkout/seleccion/', views.seleccion_pago, name='seleccion_pago'),
    path('checkout/confirmacion/', views.checkout_confirmacion, name='checkout_confirmacion'),
    path('checkout/confirmacion/invitado/', views.checkout_confirmacion_invitado, name='checkout_confirmacion_invitado'),

    # Políticas
    path('politicas-privacidad/', views.politicas_privacidad, name='politicas_privacidad'),
    path('politicas-envio/', views.politicas_envio, name='politicas_envio'),

    # Registro de usuarios
    path('registro/', views.registro, name='registro'),
]