from django.contrib import admin

# Register your models here.
from .models import Multimedia
from django.utils.html import format_html

class MultimediaAdmin(admin.ModelAdmin):
    
    list_display = ('name','img',)

    def img(self,obj):
        return format_html('<img src={} width="130" height="100" />',obj.file.url)
        

admin.site.register(Multimedia,MultimediaAdmin)
