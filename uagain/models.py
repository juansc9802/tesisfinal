from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(max_length=255, unique=True)

    def __str__(self):
        return self.nombre


class Productos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, unique=False, null=False, blank=False)
    descripcion = models.TextField(max_length=255, unique=False)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    imagen = models.ImageField(upload_to='productos/', default='productos/default.webp', null=False, blank=False)
    creador = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    aceptado = models.BooleanField(default=False)

    def clean(self):
        if self.precio is not None and self.precio<10000:
            raise ValidationError("El precio mínimo es de $10,000")
    
    def __str__(self):
        return self.nombre
# Create your models here.

class Mensaje(models.Model):
    emisor = models.ForeignKey(User, related_name='mensajes_enviados', on_delete=models.CASCADE)
    receptor = models.ForeignKey(User, related_name='mensajes_recibidos', on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'De {self.emisor.username} para {self.receptor.username} - {self.fecha}'