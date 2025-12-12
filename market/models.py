from django.db import models
from django.contrib.auth.models import User

class Producto(models.Model):
    TIPO_CHOICES = [
        ('fisico', 'Físico'),
        ('digital', 'Digital'),
    ]

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='fisico')
    archivo = models.FileField(upload_to='digitales/', blank=True, null=True)

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pedidos'
    )
    nombre = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=True, choices=[(True, 'Pendiente'), (False, 'Enviado')])

    def __str__(self):
        if self.usuario:
            return f"Pedido #{self.id} - {self.usuario.username}"
        return f"Pedido #{self.id} - {self.nombre or 'Invitado'}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True)

def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

@property
def subtotal(self):
        return self.cantidad * self.precio

class CarritoGuardado(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    datos = models.JSONField(default=dict)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return f"Perfil de {self.usuario.username}"