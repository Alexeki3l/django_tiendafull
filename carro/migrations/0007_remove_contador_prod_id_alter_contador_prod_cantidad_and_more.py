# Generated by Django 4.0.3 on 2022-05-13 02:50

import builtins
from django.db import migrations, models
import django.db.models.deletion
from tienda.models import Product


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0007_alter_producto_image_alter_producto_image1_and_more'),
        ('carro', '0006_contador_prod_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contador_prod',
            name='id',
        ),
        migrations.AlterField(
            model_name='contador_prod',
            name='cantidad',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='contador_prod',
            name='producto',
            field=models.OneToOneField( on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='tienda.producto'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contador_prod',
            name='total',
            field=models.FloatField(default=0),
        ),
    ]
