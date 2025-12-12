from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Producto, Perfil

# Formulario para productos
class ProductoForm(forms.ModelForm):
    precio = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Precio en CLP',
            'step': '1',
            'min': '0'
        })
    )

    class Meta:
        model = Producto
        fields = ['tipo', 'nombre', 'descripcion', 'precio', 'stock', 'imagen', 'archivo']
        widgets = {
            'tipo': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_tipo'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción breve'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cantidad disponible',
                'step': '1',
                'min': '0'
            }),
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'archivo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'id': 'id_archivo'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'precio' in self.initial:
            try:
                self.initial['precio'] = int(float(self.initial['precio']))
            except (ValueError, TypeError):
                self.initial['precio'] = 0

# Formulario para checkout de invitados
class CheckoutInvitadoForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre completo",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre completo'
        })
    )
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ejemplo@correo.com'
        })
    )
    direccion = forms.CharField(
        label="Dirección de envío",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Calle, número, comuna...'
        })
    )
    telefono = forms.CharField(
        label="Teléfono",
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+56 9 1234 5678'
        })
    )

# Formulario de registro personalizado
class RegistroForm(UserCreationForm):
    first_name = forms.CharField(
        label='Nombre completo',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre completo'
        })
    )
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ejemplo@correo.com'
        })
    )
    direccion = forms.CharField(
        label='Dirección',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Calle, número, comuna...'
        })
    )
    telefono = forms.CharField(
        label='Teléfono',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+56 9 1234 5678'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2', 'direccion', 'telefono']