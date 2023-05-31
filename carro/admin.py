from django.contrib import admin
from .models import Contador_Prod, Orden,StatusOrder,MethodPay,Carrito
from django.utils.html import format_html
# Register your models here.


class ContadorProdAdmin(admin.ModelAdmin):
    list_display = ('producto','img','precio','cantidad', 'total',)

    def img(self,obj):
        return format_html('<img src={} width="130" height="100" />',obj.producto.image.url )
    
    def precio(self,obj):
        return obj.producto.precio

class CarritoAdmin(admin.ModelAdmin):
    ordering    =   ('nombre','usuario','created', )
    list_display = ('nombre','usuario','created', )
    readonly_fields  = ("created",)

class StatusOrderAdmin ( admin.ModelAdmin):
    ordering    =   ('nombre','created', 'updated', )
    list_display = ('nombre','created', 'updated', )
    readonly_fields  = ('created', 'updated', )

class MethodPayAdmin ( admin.ModelAdmin):
    ordering    =   ('nombre','created', 'updated', )
    list_display = ('nombre','created', 'updated', )
    readonly_fields  = ('created', 'updated', )

class OrdenAdmin ( admin.ModelAdmin):
    ordering    =   ('carro','estado', 'metodo_pago', 'created' )
    list_display = ('carro','estado', 'metodo_pago', 'created' )
    readonly_fields  = ('created',)


admin.site.register(Carrito,CarritoAdmin)
admin.site.register(StatusOrder,StatusOrderAdmin)
admin.site.register(MethodPay,MethodPayAdmin)
admin.site.register(Orden,OrdenAdmin)
admin.site.register(Contador_Prod, ContadorProdAdmin)