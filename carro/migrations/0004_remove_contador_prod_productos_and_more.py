# Generated by Django 4.0.3 on 2022-05-12 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0007_alter_producto_image_alter_producto_image1_and_more'),
        ('carro', '0003_contador_prod_alter_carrito_productos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contador_prod',
            name='productos',
        ),
        migrations.AddField(
            model_name='contador_prod',
            name='producto',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='tienda.producto'),
        ),
        migrations.AlterField(
            model_name='contador_prod',
            name='cantidad',
            field=models.IntegerField(default=1),
        ),
    ]
