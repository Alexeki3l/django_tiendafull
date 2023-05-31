from django.urls import path

from usuarios import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import login, views as auth_views


urlpatterns = [
    
    # path('', views.Registrar_Usuarios, name="Registrar"),

    # path('login', views.Login_Usuarios, name="Login"),

    path('registrar', views.Registrar_Usuarios, name="registrar"),

    path('registrar_clientes', views.Registrar_Usuarios_Clientes, name="registrar2"),

    
    # path('autenticar', auth_views.LoginView.as_view(template_name="usuario/login.html"), name="login"),
    # # path('user_page', views.User_Page, name="user_page"),

    path('logout/', auth_views.LogoutView.as_view(template_name="InicioTiendaFull/home_landing.html"), name="logout"),

    

    
]