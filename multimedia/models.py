from django.db import models
from usuarios.models import Profile
from tienda.models import Store, Product
from django.db.models.signals import post_save


class Multimedia(models.Model):
    # id          = models.AutoField(primary_key=True, unique=False, )
    name        = models.CharField(max_length=255, null=True, blank=True)
    file        =models.FileField(default='/media/store/sin-photo.jpg')
    TYPE        = (('1', 'profile'), ('2', 'store'), ('3', 'product'),)
    type        = models.CharField(max_length=1, choices=TYPE)
    profiles    = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    stores      = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True)
    products    = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = "multimedia"
        verbose_name_plural = "multimedias"

    def __str__(self):
        return self.name
    
    def image_url(self):
        if self.file and hasattr(self.file, 'url'):
            return self.imagen.url

    def save(self, *args, **kwargs):
        # no_photo_profile = '/media/profile/sin-foto.png'
        # no_photo_store = '/media/store/sin-photo.jpg'
        # no_photo_product = '/media/store/sin-photo.jpg'
        if not self.created:
            print("CREATE")
            if self.type == "1":
                self.stores = None
                self.products = None
                self.file.field.upload_to='profile'
                # self.file = no_photo_profile
                self.name = self.file.url.split("/")[-1].split(".")[-2]
                return super().save(self,*args,**kwargs)

            elif self.type == "2":
                self.profiles = None
                self.products = None
                self.file.field.upload_to='store'
                # self.file = no_photo_store
                self.name = self.file.url.split("/")[-1].split(".")[-2]
                return super().save(self,*args,**kwargs)

            elif self.type == "3":
                self.stores = None
                self.profiles = None
                self.file.field.upload_to='product'
                # self.file = no_photo_product
                self.name = self.file.url.split("/")[-1].split(".")[-2]
                return super().save(self,*args,**kwargs)
        else:
            print("UPDATED")
            if self.type == "1":
                self.stores = None
                self.products = None
                self.file.field.upload_to='profile'
                self.name = self.file.url.split("/")[-1].split(".")[-2]
                return super(Multimedia,self).save(force_update=True)

            elif self.type == "2":
                self.profiles = None
                self.products = None
                self.file.field.upload_to='store'
                self.name = self.file.url.split("/")[-1].split(".")[-2]
                return super(Multimedia,self).save(force_update=True)

            elif self.type == "3":
                self.stores = None
                self.profiles = None
                self.file.field.upload_to='product'
                self.name = self.file.url.split("/")[-1].split(".")[-2]
                return super(Multimedia,self).save(force_update=True)
        
# def create_multimedia_store(sender, instance, created, **kwargs):
#     if created:
#         Multimedia.objects.create(stores = instance)
# post_save.connect(create_multimedia_store, sender = Store)


# def create_multimedia_profile(sender, instance, created, **kwargs):
#     if created:
#         Multimedia.objects.create(profiles = instance)
# post_save.connect(create_multimedia_profile, sender = Profile)


# def create_multimedia_product(sender, instance, created, **kwargs):
#     if created:
#         Multimedia.objects.create(products = instance)
# post_save.connect(create_multimedia_product, sender = Product)