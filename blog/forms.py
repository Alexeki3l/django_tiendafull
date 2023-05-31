

from .models import Comentario, Post, Respuesta
from . import forms
from django import forms


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comentario
        fields = ("contenido",)
        
class ReplyCommentForm(forms.ModelForm):

    class Meta:
        model  = Comentario  
        fields = ("contenido",)

class EditarComentarioForm(forms.ModelForm):

    class Meta:
        model  = Comentario  
        fields = ('contenido',)
        widgets={
            # 'titulo':forms.TextInput(attrs={'class':'form-control'}),
            # 'categorias':forms.SelectMultiple(attrs={'class':'form-control'}),
            # 'imagen':forms.TextInput(attrs={'class':'form-control'}),
            'contenido':forms.Textarea(attrs={'class':'form-control'}),
            # 'estado':forms.TextInput(attrs={'class':'form-control'}),
        }

class EditarRespuestaForm(forms.ModelForm):

    class Meta:
        model  = Respuesta  
        fields = ('contenido',)
        widgets={
            # 'titulo':forms.TextInput(attrs={'class':'form-control'}),
            # 'categorias':forms.SelectMultiple(attrs={'class':'form-control'}),
            # 'imagen':forms.TextInput(attrs={'class':'form-control'}),
            'contenido':forms.Textarea(attrs={'class':'form-control'}),
            # 'estado':forms.TextInput(attrs={'class':'form-control'}),
        }