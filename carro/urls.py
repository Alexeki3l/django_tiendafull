from django.urls import path

from . import views

app_name="carro"

urlpatterns = [
    
    path('agregar/<int:producto_id>', views.Agregar_Producto, name="agregar"),
    path('eliminar/<int:producto_id>', views.Eliminar_Producto, name="eliminar"),
    path('restar/<int:producto_id>', views.Restar_Producto, name="restar"),
    path('limpiar/', views.Limpiar_Carro, name="limpiar"),
    
    
    
]
