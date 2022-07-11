from django.contrib import admin
from .models import Faq

from django import forms
# Register your models here.


class FaqForm( forms.ModelForm ):
    # Que el charfield "contenido" se comporte como un textarea
    respuesta = forms.CharField( widget=forms.Textarea )


class FaqAdmin(admin.ModelAdmin):
    
    form = FaqForm
    ordering    =   ('pregunta','respuesta', 'created', "updated",)
    list_display = ('pregunta','respuesta', 'created', "updated",)
    readonly_fields  = ("created", "updated",)


admin.site.register(Faq,FaqAdmin)