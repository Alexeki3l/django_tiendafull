
from functools import total_ordering
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from tienda.models import Producto
from django.db.models.signals import post_save
# Create your models here.


class Contador_Prod(models.Model):
    producto  = models.OneToOneField(Producto, on_delete=models.CASCADE, primary_key=True)
    cantidad  = models.IntegerField(default= 1)
    total     = models.FloatField(default= 0)
    class Meta:
        verbose_name    = "contador"
        verbose_name_plural = "contadores"

    def __str__(self):
        return self.producto.nombre

class Carrito(models.Model):
    nombre    = models.CharField(max_length=255, null=True, blank=True)
    usuario   = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    productos = models.ManyToManyField(Contador_Prod, related_name='carro_productos', null=True, blank=True)
    created   = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name    = "carrito"
        verbose_name_plural = "carritos"

    def __str__(self):
        if self.nombre:
            return self.nombre
        else:
            self.nombre = 'Default'
            return self.nombre
    
    def get_absolute_url(self):
        return reverse("productos") 

class StatusOrder(models.Model):
    nombre    = models.CharField(max_length=100)
    created   = models.DateTimeField(auto_now_add=True)
    updated   = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name    = "estado"
        verbose_name_plural = "estados"

    def __str__(self):
        return self.nombre

class MethodPay(models.Model):
    nombre    = models.CharField(max_length=100)
    created   = models.DateTimeField(auto_now_add=True)
    updated   = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name    = "metodo"
        verbose_name_plural = "metodos"

    def __str__(self):
        return self.nombre

class Orden(models.Model):
    carro       = models.OneToOneField(Carrito, on_delete=models.CASCADE, null=True, blank=True)
    estado      = models.OneToOneField(StatusOrder, on_delete=models.CASCADE, null=True, blank=True)
    metodo_pago = models.OneToOneField(MethodPay, on_delete=models.CASCADE, null=True, blank=True)
    created     = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name    = "orden"
        verbose_name_plural = "ordenes"
        ordering = ['-created']

def create_carrito(sender, instance, created, **kwargs):
    if created:
        Contador_Prod.objects.create(producto = instance)

post_save.connect(create_carrito, sender = Producto)