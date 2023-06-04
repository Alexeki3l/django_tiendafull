from django.urls import path

from dashboard import views
from django.conf import settings
from django.conf.urls.static import static
from usuarios.views import User_Page


urlpatterns = [
    
    path('', views.Home_DashboardView, name="home_dash"),
    path('perfil/', User_Page, name="perfil"),

    # ------------------------DASHBOARD BLOGS--------------------

    path('blog/', views.BlogsView.as_view(), name="blog_dash"),
    path('blog/add', views.AddBlogView.as_view(), name="add_post"),
    path('blog/edit/<int:pk>', views.UpdateBlogView.as_view(), name="update_post"),
    path('blog/delete/<int:pk>', views.DeleteBlogView.as_view(), name="delete_post"),

    # ---------------------DASHBOARD TIENDA------------------------
    path('tiendas/', views.TiendasView.as_view(), name="tiendas_dash"),
    path('tiendas/details/<int:pk>', views.DetallesTiendaView.as_view(), name="tienda_details"),
    path('tiendas/delete/<int:pk>', views.EliminarTiendaView.as_view(), name="tienda_delete"),
    path('tiendas/editar/<int:pk>', views.EditarTiendaView.as_view(), name="update_tienda"),
    path('tiendas/add/', views.AdicionarTiendaView.as_view(), name="add_tienda"),

    # --------------------DASHBOARD PRODUCTOS--------------------
    path('productos/', views.ProductosView.as_view(), name="productos_dash"),
    path('productos/add', views.AdicionarProductoView.as_view(), name="add_producto"),
    path('productos/details/<int:pk>', views.DetallesProductoView.as_view(), name="productos_details"),
    path('productos/update/<int:pk>', views.EditarProductoView.as_view(), name="update_producto"),
    path('productos/delete/<int:pk>', views.EliminarProductoView.as_view(), name="delete_producto"),

    # --------------------DASHBOARD CLIENTES------------------------
    path('clientes/', views.ClientesView.as_view(), name="clientes_dash"),
    
]



