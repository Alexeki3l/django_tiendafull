from django.contrib import admin
from .models import TipoPerfil, Profile
from django import forms
from django.utils.html import format_html

# Register your models here.


class ContenidoModelForm( forms.ModelForm ):
    # Que el charfield "contenido" se comporte como un textarea
    bio = forms.CharField( widget=forms.Textarea )
    

class TipoPerfilAdmin(admin.ModelAdmin):
    
    ordering     = ('created',)
    list_display = ('nombre','created', 'updated', )
    readonly_fields  = ("created", "updated",)

class ProfileAdmin(admin.ModelAdmin):
    form = ContenidoModelForm
    ordering     = ('user','tipo','telf', 'direccion', 'localizacion',)
    list_display = ('user','img','tipo', 'telf', 'direccion', 'localizacion',)

    def img(self,obj):
        return format_html('<img src={} width="130" height="100" />',obj.imagen.url )
    

admin.site.register(TipoPerfil,TipoPerfilAdmin)
admin.site.register(Profile,ProfileAdmin)