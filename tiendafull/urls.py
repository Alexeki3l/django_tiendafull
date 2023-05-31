"""tiendafull URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from pathlib import Path
from urllib import request
from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import login

# from django.conf.urls import handler404
# from InicioTiendaFull.views import Error_404
# from django.http import request

urlpatterns = [

    path('admin/', admin.site.urls),

    path("tienda/",include("tienda.urls")),

    path("blog/",include("blog.urls")),

    path("user/",include("usuarios.urls")),

    path("dashboard/",include("dashboard.urls")),

    # path("user/login",include("usuarios.urls")),

    path("",include("InicioTiendaFull.urls")),

    path("accounts/",include("django.contrib.auth.urls"), name="login"),

    path('carro/', include("carro.urls")),



]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





