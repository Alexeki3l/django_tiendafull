
from gc import get_objects
from typing import List
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy, reverse
# from usuarios.forms import RegistroForm
from django.contrib import messages

from carro.models import Carrito
from .models import Profile, TipoPerfil
from .forms import UserRegisterForm, RegistrarPerfil
import socket
# Create your views here.

# Registra los usuarios de tipo Proveedor
def Registrar_Usuarios(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            # Creando un perfil de tipo Proveedor
            Profile.objects.filter(user_id = usuario.id).update(tipo_id = 2)
            login(request, usuario)
            return redirect('home_dash')
            
    else:
        form = UserRegisterForm()
    context = { "form" : form }
    
    return render (request, "usuarios/logup.html", context)

def User_Page(request):
    return render(request, "usuarios/user_page.html")

# Registra los usuarios de tipo Cliente
def Registrar_Usuarios_Clientes(request):
    ip = socket.gethostbyname(socket.gethostname())
    if request.method == "POST":
        if request.user.is_authenticated:
            form  = UserRegisterForm(request.POST)
            form2 = RegistrarPerfil(request.POST)
            if form.is_valid():
                # if form2.is_valid():
                #     usuario = form.save()
                #     login(request, usuario)
                #     # username = form.cleaned_data["username"]
                #     # messages.success(request, f"Usuario {username} creado")
                #     perfil = Profile(
                #         user_id      = usuario.id,
                #         telf         = request.POST.get('telf'),
                #         direccion    = request.POST.get('direccion'),
                #         localizacion = request.POST.get('localizacion'),
                #         tipo_id      = 1,
                #                     )
                #     perfil.save()
                    return redirect('productos')
        else:
            
            form  = UserRegisterForm(request.POST)
            form2 = RegistrarPerfil(request.POST)
            if form.is_valid():
                if form2.is_valid():
                    usuario = form.save()
                    login(request, usuario)
                    # username = form.cleaned_data["username"]
                    # messages.success(request, f"Usuario {username} creado")
                    perfil = Profile(
                        user_id      = usuario.id,
                        telf         = request.POST.get('telf'),
                        direccion    = request.POST.get('direccion'),
                        localizacion = request.POST.get('localizacion'),
                        tipo_id      = 1,
                                    )
                    perfil.save()
                    Carrito.objects.filter(nombre = f'{ip}').update(nombre =f'Carrito_de_{usuario}')
                    return redirect('productos')
            else:
                form = UserRegisterForm()
                context = { "form" : form, 'carrito' : carrito }
    else:
        if request.user.is_authenticated:
            carrito= Carrito.objects.get(usuario = request.user)
            total = 0
            cont = 0
            for producto in carrito.productos.all():
                total += producto.producto.precio
                cont += 1
        else:
            carrito= Carrito.objects.get(nombre = f'{ip}')
            total = 0
            cont = 0
            for producto in carrito.productos.all():
                total += producto.producto.precio
                cont += 1
            
        form = UserRegisterForm()
    context = { "form" : form, 'carrito' : carrito, 'total':total, 'cont':cont}
    
    return render (request, "usuarios/chequear.html", context)
    


    
        
    

     

