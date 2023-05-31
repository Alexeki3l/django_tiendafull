
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.shortcuts import redirect


# Create your models here.

class Categoria(models.Model):
    nombre  = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name    = "categoria"
        verbose_name_plural = "categorias"
    
    def __str__(self):
        return self.nombre

class Post(models.Model):
    titulo          = models.CharField(max_length=50)
    categorias      = models.ManyToManyField(Categoria, related_name='categorias')
    imagen          = models.ImageField(upload_to="blog", null=True, blank=True)
    contenido       = models.TextField(null=True, blank=True)
    autor           = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_user") 
    likes           = models.ManyToManyField(User, null=True, blank=True, related_name="post_likes")
    estado          = models.BooleanField(default=True)
    approved_post   = models.BooleanField(default=True)
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name    = "post"
        verbose_name_plural = "posts"
        ordering = ['-created']

    def __str__(self):
        return self.titulo

    def total_likes(self):
        self.likes.count()

    def get_absolute_url(self):
        return reverse('blog_dash')

    def image_url(self):
        if self.imagen and hasattr(self.imagen, 'url'):
            return self.imagen.url
    
    
class Comentario(models.Model):
    autor            = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido        = models.TextField()
    post             = models.ForeignKey(Post , on_delete=models.CASCADE, null=True, blank=True,verbose_name="post", related_name='comentarios')
    likes            = models.ManyToManyField(User, null=True, blank=True, related_name="post_comentario")
    approved_comment = models.BooleanField(default=True)
    created          = models.DateTimeField(auto_now_add=True)
    updated          = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name    = "comentario"
        verbose_name_plural = "comentarios"
        ordering = ['-created']
    
    def approve(self):
        self.approved_comment = True
        self.save()

    def total_likes(self):
        self.likes.count()

    def __str__(self):
        return self.contenido[:20]

    def get_absolute_url(self):
        # post = Post.objects.get(id = self.post.pk)
        # return reverse('commnets', self.id)
        # return redirect ("blog_full", self.post.id)
        return reverse('blog_full', kwargs={'post_id': self.post.pk})
        
class Respuesta(models.Model):
    autor            = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido        = models.TextField()
    comentarios      = models.ForeignKey(Comentario , on_delete=models.CASCADE, null=True, blank=True, verbose_name="comentario", related_name='respuestas')
    likes            = models.ManyToManyField(User, null=True, blank=True, related_name="comentario_respuesta")
    approved_comment = models.BooleanField(default=True)
    created          = models.DateTimeField(auto_now_add=True)
    updated          = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name    = "respuesta"
        verbose_name_plural = "respuestas"
        ordering = ['-created']
    
    def approve(self):
        self.approved_comment = True
        self.save()

    def total_likes(self):
        self.likes.count()
        
    def __str__(self):
        return self.contenido

    def get_absolute_url(self):
        return reverse("blog_full", kwargs={"post_id": self.comentarios.post.pk})
    
    
