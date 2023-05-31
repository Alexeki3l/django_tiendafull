from pydoc import resolve
from urllib.request import url2pathname
from wsgiref.util import request_uri
from django.shortcuts import get_object_or_404, render, redirect
from matplotlib.style import context

from carro.models import Carrito
from .models import ComentarioP, RespuestaP
from .models import Producto, CategoriaProducto
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .forms import CommentProdForm, EditarComentarioProdForm, EditarRespuestaProdForm
from django.utils import timezone
import socket

# Create your views here.

class Tienda(ListView):
    model = Producto
    template_name = 'tienda/tienda_landing.html'
    context_object_name = 'productos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # if Carrito.objects.filter(usuario = self.request.user):
        if self.request.user.is_authenticated:
            if Carrito.objects.filter(usuario = self.request.user):
                context['carrito'] = Carrito.objects.get(usuario = self.request.user)
                carrito = Carrito.objects.get(usuario = self.request.user)
                total = 0
                for producto in carrito.productos.all():
                    total += producto.total
                context['totall'] = total
                return context
            else:
                return context
        else:
            ip = socket.gethostbyname(socket.gethostname())
            carrito= Carrito.objects.filter(nombre = f'{ip}')
            if not carrito:
                return context
            else:
                carrito = Carrito.objects.get(nombre = f'{ip}')
                total = 0
                for producto in carrito.productos.all():
                    total += producto.total
                context['totall'] = total
                context['carrito'] = carrito
                return context

class DetalleProducto(DetailView):
    model = Producto
    template_name = 'tienda/detalle_producto.html'
    context_object_name = 'producto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # kwargs={'pk': self.producto.pk}
        comentarios = ComentarioP.objects.filter(producto_id = kwargs['object'])
        # for comentario in comentarios:
        #     respuestas = RespuestaP.objects.filter(comentariosp_id = comentario.id)
        cantidad_comentarios = comentarios.count()
        # cantidad_respuestas = respuestas.count()
        total = cantidad_comentarios 
        ''' + cantidad_respuestas'''
        context["total"] = total
        context['productos'] = Producto.objects.all()
        
        return context

class EditarComentarioProd(UpdateView):
    model = ComentarioP
    form_class = EditarComentarioProdForm
    template_name='tienda/editar_comments_prod.html'
    # success_url= reverse('comments', args=[str('comentario.pk')])

    def form_valid(self, form):
        form.instance.updated = timezone.now()
        form.instance.autor = self.request.user
        return super().form_valid(form)

class EditarRespuestaProd(UpdateView):
    model = RespuestaP
    form_class = EditarRespuestaProdForm
    template_name='tienda/editar_reply_prod.html'
    
    def form_valid(self, form):
        form.instance.updated = timezone.now()
        form.instance.autor = self.request.user
        return super().form_valid(form)

def add_comment_prod(request, producto_id):
        
        if request.method == 'POST':
            if request.user.profile.tipo.id == 2:
                print('ENTRA')
                form = CommentProdForm(request.POST or None)
                if form.is_valid():
                    context ={
                    
                    'form':form,
                            }
                    contenido = request.POST.get('contenido')
                    # comentario = Comentario.objects.create(autor = request.user, contenido = contenido, post = post, approved_comment = True)
                    comentario = ComentarioP(
                        autor = request.user, 
                    contenido = contenido, 
                    producto_id = producto_id, 
                    approved_comment = True
                    )
                    comentario.save()
                    return HttpResponseRedirect(reverse('productos_details', args=[str(producto_id)]))
            else:
                print('por aca')
                form = CommentProdForm(request.POST or None)
                if form.is_valid():
                    context ={
                    
                    'form':form,
                            }
                    contenido = request.POST.get('contenido')
                    # comentario = Comentario.objects.create(autor = request.user, contenido = contenido, post = post, approved_comment = True)
                    comentario = ComentarioP(
                        autor = request.user, 
                    contenido = contenido, 
                    producto_id = producto_id, 
                    approved_comment = True
                    )
                    comentario.save()
                    
                    return HttpResponseRedirect(reverse('detalle_producto', args=[str(producto_id)]))
            
        else:
            form = CommentProdForm()   
        context ={
                'form':form,
                }
            
        return HttpResponseRedirect(reverse('productos_details', args=[str(producto_id)]))

def responder_comment_prod(request, comentario_id):
    
    comentario = ComentarioP.objects.get(pk = comentario_id)
    if request.method == 'POST':
        form = CommentProdForm(request.POST or None)
        if form.is_valid():
            context ={
             
             'form':form,
                    }
            contenido = request.POST.get('contenido')
            respuesta = RespuestaP( contenido = contenido, 
                                    approved_comment = True,
                                    autor = request.user, 
                                    comentariosp_id = comentario_id )
            respuesta.save()
            # return redirect('blog_full', comentario.post_id)
            return HttpResponseRedirect(reverse('detalle_producto', args=[str(comentario.producto_id)]))
        
    else:
      form = CommentProdForm()   
    context ={
             'form':form,
            }
        
    return HttpResponseRedirect(reverse('detalle_producto', args=[str(comentario.producto_id)]))

def comment_delete(request, comentario_id):
    comentario = get_object_or_404(ComentarioP, pk=comentario_id)
    comentario.delete()
    return redirect ("detalle_producto", comentario.producto.id)

def reply_delete(request, respuesta_id):
    respuesta = get_object_or_404(RespuestaP, id=respuesta_id)
    comentario = ComentarioP.objects.get(id = respuesta.comentariosp_id)
    producto = Producto.objects.get(id = comentario.producto_id)
    respuesta.delete()
    return redirect("detalle_producto", producto.id)

def LikeProd(request, producto_id):
    producto = get_object_or_404(Producto, id = producto_id)
    producto.likes.add(request.user)
    # return redirect("blog_full", post.id)    
    return HttpResponseRedirect(reverse('detalle_producto', args=[str(producto_id)]))
    
def DislikeProd(request, producto_id):
    producto = get_object_or_404(Producto, id = producto_id)
    producto.likes.remove(request.user)
    return HttpResponseRedirect(reverse('detalle_producto', args=[str(producto_id)]))

def LikeComment(request, comentario_id):
    comentario = get_object_or_404(ComentarioP, id = comentario_id)
    comentario.likes.add(request.user)
    producto = Producto.objects.get(id = comentario.post_id)
    return redirect("detalle_producto", producto.id)

def DislikeComment(request, comentario_id):
    comentario = get_object_or_404(ComentarioP, id = comentario_id)
    comentario.likes.remove(request.user)
    producto = Producto.objects.get(id = comentario.producto_id)
    return redirect("detalle_producto", producto.id)

def LikeReply(request, respuesta_id):
    respuesta = get_object_or_404(RespuestaP, id = respuesta_id)
    respuesta.likes.add(request.user)
    comentario = ComentarioP.objects.get(id = respuesta.comentariosp_id)
    producto = Producto.objects.get(id = comentario.producto_id)
    return redirect("detalle_producto", producto.id)

def DislikeReply(request, respuesta_id):
    respuesta = get_object_or_404(RespuestaP, id = respuesta_id)
    respuesta.likes.add(request.user)
    comentario = ComentarioP.objects.get(id = respuesta.comentariosp_id)
    producto = Producto.objects.get(id = comentario.producto_id)
    return redirect(reverse("detalle_producto",args=[str(producto.id)]))


# --------------------------CARRO---------------------------------


        
    
   


    