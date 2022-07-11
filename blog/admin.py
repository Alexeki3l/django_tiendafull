from django.contrib import admin
from .models import Post, Categoria, Comentario, Respuesta
from django import forms
from django.utils.html import format_html

# Register your models here.
class ContenidoModelForm( forms.ModelForm ):
    # Que el charfield "contenido" se comporte como un textarea
    contenido = forms.CharField( widget=forms.Textarea )
    

class PostAdmin(admin.ModelAdmin):
    
    form = ContenidoModelForm
    ordering    =   ('titulo','autor', 'created', )
    list_display = ('titulo','autor', 'img','created', )
    readonly_fields  = ("created", "updated",)

    def img(self,obj):
        return format_html('<img src={} width="130" height="100" />',obj.imagen.url )

class CategoriaAdmin(admin.ModelAdmin):

    ordering     = ('nombre',)
    list_display = ('nombre','created', 'updated', )
    readonly_fields  = ("created", "updated",)

class ComentarioAdmin(admin.ModelAdmin):
    form    = ContenidoModelForm
    ordering     = ('autor', 'created',)
    list_display = ('autor','contenido', 'post', 'approved_comment', 'created',  )
    readonly_fields  = ("created", "updated",)

class RespuestaAdmin(admin.ModelAdmin):
    form    = ContenidoModelForm
    ordering     = ('autor', 'created',)
    list_display = ('autor','contenido', 'approved_comment', 'created',  )
    readonly_fields  = ("created", "updated",)


admin.site.register(Post,PostAdmin)
admin.site.register(Categoria,CategoriaAdmin)
admin.site.register(Comentario,ComentarioAdmin)
admin.site.register(Respuesta,RespuestaAdmin)
