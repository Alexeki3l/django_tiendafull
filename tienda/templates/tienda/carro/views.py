from django.shortcuts import get_object_or_404, render

from carro.models import Carrito, Contador_Prod
from .carro import Carro
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from tienda.models import Producto
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.utils import timezone
# Create your views here.

def Agregar_Producto(request, producto_id):
    producto = Producto.objects.get(id = producto_id)
    if not Carrito.objects.filter(usuario = request.user):
        carrito = Carrito(
            nombre = f'Default Create_{request.user}',
            usuario = request.user,
            created = timezone.now()
        )     
        carrito.save()
        product = Contador_Prod(
                    producto = producto,
                    cantidad = 1,
                    total    = producto.precio,
        )
        product.save()
        carrito.productos.add(product)
        print('SEA CREA EL CARRITO Y UN CONTADOR')
        return redirect('productos')
    else:
        carrito = Carrito.objects.get(usuario = request.user)
        for product in carrito.productos.all():
            if product.producto.id == producto_id:
                print('SI SE ENCUENTRA AHI')
                Contador_Prod.objects.filter(producto = product.producto).update(
                    cantidad = product.cantidad + 1,
                    total = ( product.cantidad + 1 ) * product.producto.precio
                    ) 
                
                break
            else:
                product = Contador_Prod(
                    producto = producto,
                    cantidad = 1,
                    total    = producto.precio,
                        )
                product.save()
                carrito.productos.add(product)
        
        return redirect('productos')
        # Contador_Prod.objects.filter(producto = prod.producto).update(cantidad = prod.cantidad + 1) 
        # Contador_Prod.objects.filter(producto = prod.producto).update(total = ( prod.cantidad + 1 ) * prod.producto.precio)
            
def Restar_Producto(request,producto_id):
    carrito = Carrito.objects.get(usuario = request.user)
    producto = Producto.objects.get(id = producto_id)
    for product in carrito.productos.all():
        if product.cantidad > 1:
            if product.producto.id == producto_id:
                print('SI SE ENCUENTRA AHI')
                
                Contador_Prod.objects.filter(producto = product.producto).update(
                    cantidad = product.cantidad - 1,
                    total = ( product.cantidad - 1 ) * product.producto.precio
                    ) 
                print('Resto uno')
                   
                
        elif product.cantidad == 1:
            contador = Contador_Prod.objects.get(producto = producto)
            contador.delete()
            print('Elimino la instancia')  
            break 
    return redirect('productos')   

def Eliminar_Producto(request, producto_id):
    producto = Producto.objects.get(id = producto_id)
    contador = Contador_Prod.objects.get(producto = producto)
    contador.delete()
    print('SE ELIMINO EL PRODUCTO')         
    return redirect('productos') 

def Limpiar_Carro(request):
    contador = Contador_Prod.objects.all()
    contador.delete()
    print('SE ELIMINO TODOS LOS PRODUCTO')  
    carrito = Carrito.objects.filter(usuario = request.user)
    carrito.delete()
    print('SE ELIMINO EL CARRO') 
    return redirect('productos')
            



