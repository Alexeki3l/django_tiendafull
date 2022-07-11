from django.shortcuts import render
from django.views.defaults import page_not_found
from .models import Faq
from django.views.generic import ListView


# Create your views here.

def Home(request):
    return render(request, "InicioTiendaFull/home_landing.html")

class FaqView(ListView):
    model = Faq
    template_name = 'InicioTiendaFull/FAQ_landing.html'
    context_object_name = 'faqs'

def Contactos(request):
    return render(request, "InicioTiendaFull/contact_landing.html")

# def Error_404(request):
#     pages_404_alt="pages-404-alt.html"
#     return render(request, "InicioTiendaFull/pages-404-alt.html")
