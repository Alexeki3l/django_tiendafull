from django.urls import path

from InicioTiendaFull import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    
    path('', views.Home, name="Home"),
    path('faq/', views.FaqView.as_view(), name="Faq"),
    path('contacts/', views.Contactos, name="Contactos"),
    # path('error_404/', views.Error_404, name="Not_Found"),
    
]



