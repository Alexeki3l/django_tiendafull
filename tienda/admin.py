from django.contrib import admin
from django import forms
from .models import Cliente, Store, Product, CategoriaProducto, CategoriaTienda, ComentarioP, RespuestaP
from django.utils.html import format_html

# Register your models here.

class ContenidoModelForm( forms.ModelForm ):
    # Que el charfield "contenido" se comporte como un textarea
    descripcion = forms.CharField( widget=forms.Textarea )
    

class ContentModelForm( forms.ModelForm ):
    # Que el charfield "contenido" se comporte como un textarea
    contenido = forms.CharField( widget=forms.Textarea )

class CategoriaTiendaAdmin(admin.ModelAdmin):
    
    # form = ContenidoModelForm
    ordering     = ('nombre','created', 'updated', )
    list_display = ('nombre','created', 'updated', )
    readonly_fields  = ("created", "updated",)

class CategoriaProductoAdmin(admin.ModelAdmin):
    
    # form = ContenidoModelForm
    ordering     = ('nombre','created', 'updated', )
    list_display = ('nombre','created', 'updated', )
    readonly_fields  = ("created", "updated",)

class TiendaAdmin(admin.ModelAdmin):
    
    # form = ContenidoModelForm
    ordering     = ('nombre','encargado','direccion','created', 'updated', )
    list_display = ('nombre','img','encargado','direccion','created', 'updated', )
    readonly_fields  = ("created", "updated",)

    def img(self,obj):
        try:
            photo = obj.multimedia_set.all()[0]
            if photo.file and hasattr(photo.file, 'url'):
                return format_html('<img src={} width="130" height="100" />',photo.file.url)
        except IndexError:
            no_photo = '/media/store/sin-photo.jpg'
            return format_html('<img src={} width="130" height="100" />',no_photo)
class ProductoAdmin(admin.ModelAdmin):
    
    form = ContenidoModelForm
    ordering     = ('nombre','precio','precio_old', 'cantidad','created', 'updated', )
    list_display = ('nombre', 'precio','precio_old','cantidad','created', 'updated', )
    readonly_fields  = ("created", "updated",)

    def img(self,obj):
        images = obj.multimedia_set.all()
        list_photo = []
        for image in images:
            if image.file and hasattr(image.file, 'url'):
                list_photo.append(format_html('<img src={} width="130" height="100" />',image.file.url))
            else:
                list_photo.append(format_html('<img src={} width="130" height="100" />','/media/perfil/sin-foto.png'))
        return set(list_photo)        
        

class ComentarioProductoAdmin(admin.ModelAdmin):
    form = ContentModelForm
    ordering     = ('autor','contenido','producto','approved_comment', 'created', 'updated',)
    list_display = ('autor','contenido','producto','approved_comment', 'created', 'updated',)
    readonly_fields  = ("created", "updated",)

class RespuestasProductoAdmin(admin.ModelAdmin):
    form = ContentModelForm
    ordering     = ('autor','contenido','approved_comment', 'created', 'updated',)
    list_display = ('autor','contenido','approved_comment', 'created', 'updated',)
    readonly_fields  = ("created", "updated",)

class ClienteAdmin(admin.ModelAdmin):
    
    # form = ContenidoModelForm
    ordering     = ('person','created', )
    list_display = ('person','created', )
    readonly_fields  = ("created",)



admin.site.register(CategoriaTienda,CategoriaTiendaAdmin)
admin.site.register(CategoriaProducto,CategoriaProductoAdmin)
admin.site.register(Store,TiendaAdmin)
admin.site.register(Product,ProductoAdmin)
admin.site.register(ComentarioP,ComentarioProductoAdmin)
admin.site.register(RespuestaP,RespuestasProductoAdmin)
admin.site.register(Cliente, ClienteAdmin)