from turtle import update
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy

# Create your models here.

class CategoriaTienda(models.Model):
    nombre  = models.CharField(max_length=180)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name    = "categoria_t"
        verbose_name_plural = "categorias_t"
        ordering = ['-created']
    
    def __str__(self):
        return self.nombre

class CategoriaProducto(models.Model):
    nombre   = models.CharField(max_length= 150)
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name    = "categoria_p"
        verbose_name_plural = "categorias_p"
    
    def __str__(self):
        return self.nombre

class Tienda(models.Model):
    nombre      = models.CharField(max_length=150)
    descripcion = models.TextField()
    direccion   = models.CharField(max_length=300)
    encargado   = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen      = models.ImageField(upload_to='tienda')
    categorias  = models.ManyToManyField(CategoriaTienda, null=True, blank=True, related_name='categorias_tienda')
    open        = models.BooleanField(default=True)
    likes       = models.ManyToManyField(User, null=True, blank=True, related_name='tienda_likes' )
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name    = "tienda"
        verbose_name_plural = "tiendas"
        ordering = ['-created']


    def __str__(self):
        return self.nombre

    def total_likes(self):
        self.likes.count()

    def get_absolute_url(self):
        return reverse('tiendas_dash')

    def image_url(self):
        if self.imagen and hasattr(self.imagen, 'url'):
            return self.imagen.url
   
class Producto(models.Model):
    nombre          = models.CharField(max_length=50)
    precio          = models.FloatField()
    precio_old      = models.FloatField(blank=True, null=True)
    descripcion     = models.TextField(max_length=1000)
    image           = models.ImageField(upload_to='producto')
    image1          = models.ImageField(upload_to='producto')
    image2          = models.ImageField(upload_to='producto')
    tienda          = models.ForeignKey(Tienda, null=True, blank=True, on_delete=models.CASCADE)
    cantidad        = models.IntegerField()
    vender          = models.BooleanField(default= True)
    categorias      = models.ManyToManyField(CategoriaProducto, related_name='categorias_p')
    likes           = models.ManyToManyField(User, null=True, blank=True, related_name='producto_likes' )
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name    = "producto"
        verbose_name_plural = "productos"
        ordering = ['-created']

    def __str__(self):
        return self.nombre

    def total_likes(self):
        self.likes.count()

    def get_absolute_url(self):
        return reverse('productos_details', kwargs={'pk': self.pk})

    def image_url(self):
        if self.imagen and hasattr(self.imagen, 'url'):
            return self.imagen.url

class Cliente(models.Model):
    person    = models.OneToOneField(User, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, related_name='productos_clientes')
    created   = models.DateField(auto_now_add=True)
    class Meta:
        verbose_name    = "cliente"
        verbose_name_plural = "clientes"
        ordering = ['-created']

    def __str__(self):
        return f'{self.person.first_name} {self.person.last_name}'

    # def get_absolute_url(self):
    #     return reverse('productos_details', kwargs={'pk': self.pk})

# ------Comentario de los productos y sus respuestas------------------
class ComentarioP(models.Model):
    autor            = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido        = models.TextField()
    producto         = models.ForeignKey(Producto , on_delete=models.CASCADE, null=True, blank=True,verbose_name="producto", related_name='comentariosp')
    likes            = models.ManyToManyField(User, null=True, blank=True, related_name="producto_comentario")
    approved_comment = models.BooleanField(default=True)
    created          = models.DateTimeField(auto_now_add=True)
    updated          = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name    = "comentariop"
        verbose_name_plural = "comentariops"
        ordering = ['-created']
    
    def approve(self):
        self.approved_comment = True
        self.save()

    def total_likes(self):
        self.likes.count()

    def __str__(self):
        return self.contenido[:20]

    def get_absolute_url(self):
        return reverse('productos_details', kwargs={'pk': self.producto.pk})
        
class RespuestaP(models.Model):
    autor            = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido        = models.TextField()
    comentariosp      = models.ForeignKey(ComentarioP , on_delete=models.CASCADE, null=True, blank=True, verbose_name="comentariop", related_name='respuestasp')
    likes            = models.ManyToManyField(User, null=True, blank=True, related_name="comentariop_respuestap")
    approved_comment = models.BooleanField(default=True)
    created          = models.DateTimeField(auto_now_add=True)
    updated          = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name    = "respuestap"
        verbose_name_plural = "respuestasp"
        ordering = ['-created']
    
    def approve(self):
        self.approved_comment = True
        self.save()

    def total_likes(self):
        self.likes.count()
        
    def __str__(self):
        return self.contenido

    def get_absolute_url(self):
        return reverse("productos_details", kwargs={"pk": self.comentariosp.producto.pk})
# ----------------------------------------------------------------------
# ------Comentario de las tiendas y respuestas de los mismos-----------
'''class ComentarioT(models.Model):
    autor            = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido        = models.TextField()
    tienda           = models.ForeignKey(Tienda , on_delete=models.CASCADE, null=True, blank=True, verbose_name="tienda", related_name='comentariost')
    likes            = models.ManyToManyField(User, null=True, blank=True, related_name="tienda_comentario")
    approved_comment = models.BooleanField(default=True)
    created          = models.DateTimeField(auto_now_add=True)
    updated          = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name    = "comentariot"
        verbose_name_plural = "comentariost"
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
        
class RespuestaT(models.Model):
    autor            = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido        = models.TextField()
    comentariost      = models.ForeignKey(ComentarioT , on_delete=models.CASCADE, null=True, blank=True, verbose_name="comentariot", related_name='respuestast')
    likes            = models.ManyToManyField(User, null=True, blank=True, related_name="comentariot_respuestat")
    approved_comment = models.BooleanField(default=True)
    created          = models.DateTimeField(auto_now_add=True)
    updated          = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name    = "respuestat"
        verbose_name_plural = "respuestast"
        ordering = ['-created']
    
    def approve(self):
        self.approved_comment = True
        self.save()

    def total_likes(self):
        self.likes.count()
        
    def __str__(self):
        return self.contenido

    def get_absolute_url(self):
        return reverse("blog_full", kwargs={"post_id": self.comentarios.post.pk})'''
# --------------------------------------------------------------------- 
     



