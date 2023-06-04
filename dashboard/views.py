from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from numpy import product
from blog.models import Comentario, Post, Categoria
from tienda.models import Product, Store, CategoriaProducto, CategoriaTienda, Cliente
from multimedia.models import Multimedia
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from .forms import EditPostForm, EditProductoForm, AddProductoView, AddTiendaView, EditTiendaForm
from django.utils.decorators import method_decorator
from .decorators import proveedor_required



# Create your views here.
# -----------------Blogs------------------
#edit user in django?

@login_required
def Home_DashboardView(request):
    a = int(request.user.profile.tipo)
    if a == 1:
        return render(request, "Dashboard/base_dash.html")
    else:
        return redirect('Home')

class BlogsView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'Dashboard/blog/blogs.html'
    context_object_name= 'posts'

    @method_decorator(proveedor_required)
    def dispatch(self, request, *args, **kwargs):
        return super(BlogsView, self).dispatch(request, *args, **kwargs)


class AddBlogView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'Dashboard/blog/add_blog.html'
    fields=('titulo','categorias', 'imagen', 'contenido', 'estado',)

    @method_decorator(proveedor_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AddBlogView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categorias"] = Categoria.objects.all()
        return context
    

class UpdateBlogView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = EditPostForm
    template_name = 'Dashboard/blog/update_blog.html'

    @method_decorator(proveedor_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateBlogView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.updated = timezone.now()
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categorias"] = Categoria.objects.all()
        return context

class DeleteBlogView(LoginRequiredMixin,DeleteView):
    model = Post
    template_name = "Dashboard/blog/delete_blog.html"
    success_url = reverse_lazy('blog_dash')

    @method_decorator(proveedor_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DeleteBlogView, self).dispatch(request, *args, **kwargs)
    
# ------------------------------------------------------
# ----------------------Tienda--------------------------

class TiendasView(LoginRequiredMixin, ListView):
    model = Store
    template_name = 'Dashboard/tienda/tiendas.html'
    context_object_name= 'tiendas'

    @method_decorator(proveedor_required)
    def dispatch(self, request, *args, **kwargs):
        return super(TiendasView, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        dicc_aux = {}
        for tienda in context['tiendas']:
            try:
                media_obj = tienda.multimedia_set.all().first()
                if media_obj.file and hasattr(media_obj.file, 'url'):
                    dicc_aux[f'{media_obj.file.url}'] = media_obj
                    # dicc_aux[f'{tienda}'] = media_obj.file.url

            except AttributeError:
                # list_aux.append('/media/store/sin-photo.jpg' )
                multimedia = Multimedia(stores = tienda, type = "2")
                multimedia.save()
                dicc_aux['/media/store/sin-photo.jpg'] = multimedia
            # finally:
        
        context['stores'] = dicc_aux
        return context
        
class DetallesTiendaView(LoginRequiredMixin, DetailView):
    model = Store
    template_name = 'Dashboard/tienda/detalles_tienda.html'
    context_object_name = 'store'  

    @method_decorator(proveedor_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DetallesTiendaView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["productos"] = Product.objects.filter(tienda_id = context['store'].id)
        context["multimedia"] = Multimedia.objects.get(stores = context['store'].id)
        return context

class AdicionarTiendaView(LoginRequiredMixin, CreateView):
    model = Store
    form_class = AddTiendaView
    template_name = 'Dashboard/tienda/add_tienda.html'

    def form_valid(self, form):
        form.instance.created = timezone.now()
        form.instance.encargado = self.request.user
        return super().form_valid(form)

class EliminarTiendaView(LoginRequiredMixin, DeleteView):
    model = Store
    template_name = 'Dashboard/tienda/delete_tienda.html'
    success_url = reverse_lazy('tiendas_dash')


class EditarTiendaView(LoginRequiredMixin, UpdateView):
    model = Store
    form_class = EditTiendaForm
    template_name = 'Dashboard/tienda/update_tienda.html'
    # success_url = reverse_lazy('update_tienda')

    def form_valid(self, form):
        form.instance.updated  = timezone.now()
        return super().form_valid(form)


#---------------------------------------------------------- 
# -------------------Productos---------------------------

class ProductosView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'Dashboard/producto/productos.html'
    context_object_name= 'productos' 

    @method_decorator(proveedor_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductosView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categorias_productos"] = CategoriaProducto.objects.all()
        context["tiendas"] = Store.objects.all()
        return context

class DetallesProductoView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'Dashboard/producto/detalles_producto.html'
    context_object_name = 'producto'

    @method_decorator(proveedor_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DetallesProductoView, self).dispatch(request, *args, **kwargs)

class EditarProductoView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = EditProductoForm
    template_name = 'Dashboard/producto/update_producto.html'

    @method_decorator(proveedor_required)
    def dispatch(self, request, *args, **kwargs):
        return super(EditarProductoView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.updated  = timezone.now()
        return super().form_valid(form)

class EliminarProductoView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "Dashboard/producto/delete_producto.html"
    success_url = reverse_lazy('productos_dash')

    @method_decorator(proveedor_required)
    def dispatch(self, request, *args, **kwargs):
        return super(EliminarProductoView, self).dispatch(request, *args, **kwargs)

class AdicionarProductoView(LoginRequiredMixin, CreateView):
    model = Product
    # form_class = AddProductoView
    template_name = 'Dashboard/producto/add_producto.html'
    fields=('nombre','precio','categorias','tienda',
            'descripcion','cantidad','vender',)

    @method_decorator(proveedor_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AdicionarProductoView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tiendas"] = Store.objects.all()
        context["categorias"] = CategoriaProducto.objects.all()
        return context

#---------------------------------------------------------- 
# -----------------------Clientes---------------------------

class ClientesView(LoginRequiredMixin, ListView):
    model               = Cliente
    template_name       = 'Dashboard/cliente/clientes.html'
    context_object_name = 'clientes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clientes = Cliente.objects.all()
        
        if Store.objects.filter(encargado = self.request.user):
            tienda = Store.objects.get(encargado = self.request.user)
            if Product.objects.filter(tienda = tienda):
                productos = Product.objects.filter(tienda = tienda)
                for producto in productos:
                    for cliente in clientes:
                        for produc in cliente.productos.all():
                            if produc == producto:
                                context['cliente'] = cliente.productos.all()
        return context




    

    




