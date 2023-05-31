from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from numpy import product
from blog.models import Comentario, Post, Categoria
from tienda.models import Producto, Tienda, CategoriaProducto, CategoriaTienda, Cliente
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
    model = Tienda
    template_name = 'Dashboard/tienda/tiendas.html'
    context_object_name= 'tiendas'

    @method_decorator(proveedor_required)
    def dispatch(self, request, *args, **kwargs):
        return super(TiendasView, self).dispatch(request, *args, **kwargs)

class DetallesTiendaView(LoginRequiredMixin, DetailView):
    model = Tienda
    template_name = 'Dashboard/tienda/detalles_tienda.html'
    context_object_name = 'tienda'  

    @method_decorator(proveedor_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DetallesTiendaView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["productos"] = Producto.objects.filter(tienda_id = context['tienda'].id)
        return context

class AdicionarTiendaView(LoginRequiredMixin, CreateView):
    model = Tienda
    form_class = AddTiendaView
    template_name = 'Dashboard/tienda/add_tienda.html'

    def form_valid(self, form):
        form.instance.created = timezone.now()
        form.instance.encargado = self.request.user
        return super().form_valid(form)

class EliminarTiendaView(LoginRequiredMixin, DeleteView):
    model = Tienda
    template_name = 'Dashboard/tienda/delete_tienda.html'
    success_url = reverse_lazy('tiendas_dash')


class EditarTiendaView(LoginRequiredMixin, UpdateView):
    model = Tienda
    form_class = EditTiendaForm
    template_name = 'Dashboard/tienda/update_tienda.html'

    def form_valid(self, form):
        form.instance.updated  = timezone.now()
        return super().form_valid(form)


#---------------------------------------------------------- 
# -------------------Productos---------------------------

class ProductosView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'Dashboard/producto/productos.html'
    context_object_name= 'productos' 

    @method_decorator(proveedor_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductosView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categorias_productos"] = CategoriaProducto.objects.all()
        context["tiendas"] = Tienda.objects.all()
        return context

class DetallesProductoView(LoginRequiredMixin, DetailView):
    model = Producto
    template_name = 'Dashboard/producto/detalles_producto.html'
    context_object_name = 'producto'

    @method_decorator(proveedor_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DetallesProductoView, self).dispatch(request, *args, **kwargs)

class EditarProductoView(LoginRequiredMixin, UpdateView):
    model = Producto
    form_class = EditProductoForm
    template_name = 'Dashboard/producto/update_producto.html'

    @method_decorator(proveedor_required)
    def dispatch(self, request, *args, **kwargs):
        return super(EditarProductoView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.updated  = timezone.now()
        return super().form_valid(form)

class EliminarProductoView(LoginRequiredMixin, DeleteView):
    model = Producto
    template_name = "Dashboard/producto/delete_producto.html"
    success_url = reverse_lazy('productos_dash')

    @method_decorator(proveedor_required)
    def dispatch(self, request, *args, **kwargs):
        return super(EliminarProductoView, self).dispatch(request, *args, **kwargs)

class AdicionarProductoView(LoginRequiredMixin, CreateView):
    model = Producto
    # form_class = AddProductoView
    template_name = 'Dashboard/producto/add_producto.html'
    fields=('nombre','precio','categorias','tienda',
            'image','image1','image2',
            'descripcion','cantidad','vender',)

    @method_decorator(proveedor_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AdicionarProductoView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tiendas"] = Tienda.objects.all()
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
        
        if Tienda.objects.filter(encargado = self.request.user):
            tienda = Tienda.objects.get(encargado = self.request.user)
            if Producto.objects.filter(tienda = tienda):
                productos = Producto.objects.filter(tienda = tienda)
                for producto in productos:
                    for cliente in clientes:
                        for produc in cliente.productos.all():
                            if produc == producto:
                                context['cliente'] = cliente.productos.all()
        return context




    

    




