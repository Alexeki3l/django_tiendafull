from . import forms
from django import forms
from .models import ComentarioP, RespuestaP

class CommentProdForm(forms.ModelForm):
    class Meta:
        model = ComentarioP
        fields = ("contenido",)

class EditarComentarioProdForm(forms.ModelForm):

    class Meta:
        model  = ComentarioP 
        fields = ('contenido',)
        widgets={
            # 'titulo':forms.TextInput(attrs={'class':'form-control'}),
            # 'categorias':forms.SelectMultiple(attrs={'class':'form-control'}),
            # 'imagen':forms.TextInput(attrs={'class':'form-control'}),
            'contenido':forms.Textarea(attrs={'class':'form-control'}),
            # 'estado':forms.TextInput(attrs={'class':'form-control'}),
        }

class EditarRespuestaProdForm(forms.ModelForm):

    class Meta:
        model  = RespuestaP 
        fields = ('contenido',)
        widgets={
            # 'titulo':forms.TextInput(attrs={'class':'form-control'}),
            # 'categorias':forms.SelectMultiple(attrs={'class':'form-control'}),
            # 'imagen':forms.TextInput(attrs={'class':'form-control'}),
            'contenido':forms.Textarea(attrs={'class':'form-control'}),
            # 'estado':forms.TextInput(attrs={'class':'form-control'}),
        }

