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
        # var = obj.image_url
        try:
            photo = obj.multimedia_set.all()[0]
            if photo.file and hasattr(photo.file, 'url'):
                return format_html('<img src={} width="130" height="100" />',photo.file.url)
        except:
            return format_html('<img src={} width="130" height="100" />','/media/perfil/sin-foto.png')
            

    

admin.site.register(TipoPerfil,TipoPerfilAdmin)
admin.site.register(Profile,ProfileAdmin)