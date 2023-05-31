from django import forms

from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    # username = forms.CharField(label="Usuario", widget=forms.TextInput(attrs={'class' : 'u-border-1 u-border-grey-10 u-grey-10 u-input u-input-rectangle u-radius-20'}))
    # first_name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'u-border-1 u-border-grey-10 u-grey-10 u-input u-input-rectangle u-radius-20'}))
    # last_name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'u-border-1 u-border-grey-10 u-grey-10 u-input u-input-rectangle u-radius-20'}))
    # email = forms.EmailField(widget=forms.EmailField(attrs={'class' : 'u-border-1 u-border-grey-10 u-grey-10 u-input u-input-rectangle u-radius-20'}))
    # password1 = forms.PasswordInput(widget=forms.PasswordInput(attrs={'class' : 'u-border-1 u-border-grey-10 u-grey-10 u-input u-input-rectangle u-radius-20'}))
    # password2 = forms.PasswordInput(widget=forms.PasswordInput(attrs={'class' : 'u-border-1 u-border-grey-10 u-grey-10 u-input u-input-rectangle u-radius-20'}))

    class Meta:

        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

        labels = {
            "username":"Usuario",
            "first_name":"Nombre",
            "last_name":"Apellidos",
            "email":"Email",
            "password1":"Contraseña",
            "password2":"Confirmar Contraseña",
        }
            

class RegistrarPerfil(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "telf",
            "direccion",
            "localizacion",
            
        ]

        labels = {
            "telf":"Telefono",
            "direccion":"Direccion",
            "localizacion":"localizacion",
            
        }


