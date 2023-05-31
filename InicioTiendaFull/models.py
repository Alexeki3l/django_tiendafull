from ssl import create_default_context
from django.db import models
from django.urls import reverse

# Create your models here.

class Faq(models.Model):
    pregunta  = models.CharField(max_length=100)
    respuesta = models.TextField(max_length=1000)
    created   = models.DateTimeField(auto_now_add=True)
    updated   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def get_absolute_url(self):
        return reverse('Home')
