
from matplotlib import widgets
from blog.models import Post
from tienda.models import Product, Store
from . import forms
from django import forms

        
class EditPostForm(forms.ModelForm):

    class Meta:
        model  = Post  
        fields = ('titulo','categorias','contenido','estado')
        widgets={
            'titulo':forms.TextInput(attrs={'class':'form-control'}),
            'categorias':forms.SelectMultiple(attrs={'class':'form-control'}),
            # 'imagen':forms.TextInput(attrs={'class':'form-control'}),
            'contenido':forms.Textarea(attrs={'class':'form-control'}),
            # 'estado':forms.TextInput(attrs={'class':'form-control'}),
        }

class EditProductoForm(forms.ModelForm):
    class Meta:
        model  = Product
        fields = ('nombre','precio','tienda','descripcion','cantidad',)
        widgets={
            'nombre':forms.TextInput(attrs={'class':'form-control'}),
            # 'precio':forms.FloatField(attrs={'class':'form-control'}),
            # 'image':forms.ImageField(attrs={'class':'form-control'}),
            # 'image1':forms.ImageField(attrs={'class':'form-control'}),
            # 'image2':forms.ImageField(attrs={'class':'form-control'}),
            'descripcion':forms.Textarea(attrs={'class':'form-control'}),
            # 'instock':forms.BooleanField(attrs={'class':'form-control'}),
        }
        
class AddProductoView(forms.ModelForm):
    class Meta:
        model  = Product
        # fields = ('nombre','precio','image','image','image1','image2','descripcion','tienda_id','instock',)
        fields = ('__all__')
        widgets={
            'nombre':forms.TextInput(attrs={'class':'form-control'}),
            # 'precio':forms.FloatField(attrs={'class':'form-control'}),
            # 'image':forms.ImageField(attrs={'class':'form-control'}),
            # 'image1':forms.ImageField(attrs={'class':'form-control'}),
            # 'image2':forms.ImageField(attrs={'class':'form-control'}),
            'descripcion':forms.Textarea(attrs={'class':'form-control'}),
            # 'instock':forms.BooleanField(attrs={'class':'form-control'}),
        }


class AddTiendaView(forms.ModelForm):
    class Meta:
        model  = Store  
        fields = ('nombre','descripcion','direccion','categorias','is_open',)
        # fields = ('__all__')
        widgets={
            'nombre':forms.TextInput(attrs={'class':'form-control'}),
            'direccion':forms.TextInput(attrs={'class':'form-control'}),
            # 'precio':forms.FloatField(attrs={'class':'form-control'}),
            # 'image':forms.ImageField(attrs={'class':'form-control'}),
            # 'image1':forms.ImageField(attrs={'class':'form-control'}),
            # 'image2':forms.ImageField(attrs={'class':'form-control'}),
            'descripcion':forms.Textarea(attrs={'class':'form-control'}),
            # 'instock':forms.BooleanField(attrs={'class':'form-control'}),
        }
        
class EditTiendaForm(forms.ModelForm):
    class Meta:
        model  = Store  
        fields = ('nombre','direccion','descripcion','is_open',)
        widgets={
            'nombre':forms.TextInput(attrs={'class':'form-control'}),
            'direccion':forms.TextInput(attrs={'class':'form-control'}),
            # 'imagen':forms.ImageField(attrs={'class':'form-control'}),
            'descripcion':forms.Textarea(attrs={'class':'form-control'}),
            # 'is_open':forms.BooleanField(attrs={'class':'form-control'}),
        }