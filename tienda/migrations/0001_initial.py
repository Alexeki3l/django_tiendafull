# Generated by Django 4.0.3 on 2022-04-19 09:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaProducto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='CategoriaTienda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=80)),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Tienda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=300)),
                ('image', models.ImageField(upload_to='')),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField()),
                ('encargado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('precio', models.FloatField()),
                ('precio_anterior', models.FloatField(blank=True, null=True)),
                ('image', models.ImageField(upload_to='')),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField()),
                ('categorias', models.ManyToManyField(to='tienda.categoriaproducto')),
                ('tiendas', models.ManyToManyField(to='tienda.tienda')),
            ],
        ),
    ]
