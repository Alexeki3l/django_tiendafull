from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Trabajo con señales
from django.db.models.signals import post_save

# Create your models here.
class TipoPerfil(models.Model):
    nombre  = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name    = "tipoperfil"
        verbose_name_plural = "tipoperfiles"
        ordering = ['-created']

    def __str__(self):
        return self.nombre


class Profile(models.Model):
    TIPE_VALUES = (
        (1, 'Proveedor'),
        (2, 'Cliente'),
    )
    user         = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # tipo         = models.ForeignKey(TipoPerfil,null=True, blank=True, on_delete=models.CASCADE)
    tipo         = models.IntegerField(choices=TIPE_VALUES, default=1)
    imagen       = models.ImageField(upload_to='perfil',null=True, blank=True, default='sin-foto.jpg')
    bio          = models.TextField(null=True, blank=True)
    telf         = models.CharField(max_length=15, null=True, blank=True)
    direccion    = models.TextField(null=True, blank=True)
    localizacion = models.TextField(null=True, blank=True)


    class Meta:
        verbose_name    = "profile"
        verbose_name_plural = "profiles"
        

    def __str__(self):
        return f'Perfil de {self.user.username}'

    def image_url(self):
        if self.imagen and hasattr(self.imagen, 'url'):
            return self.imagen.url

def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)

post_save.connect(create_profile, sender = User)

    
    