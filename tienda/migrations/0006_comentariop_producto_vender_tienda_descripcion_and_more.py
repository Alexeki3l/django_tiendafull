# Generated by Django 4.0.3 on 2022-05-03 03:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tienda', '0005_remove_producto_instock_producto_cantidad'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComentarioP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenido', models.TextField()),
                ('approved_comment', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True, null=True, related_name='producto_comentario', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'comentariop',
                'verbose_name_plural': 'comentariops',
                'ordering': ['-created'],
            },
        ),
        migrations.AddField(
            model_name='producto',
            name='vender',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='tienda',
            name='descripcion',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='categoriaproducto',
            name='nombre',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='categoriatienda',
            name='nombre',
            field=models.CharField(max_length=180),
        ),
        migrations.AlterField(
            model_name='tienda',
            name='nombre',
            field=models.CharField(max_length=150),
        ),
        migrations.CreateModel(
            name='RespuestaP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenido', models.TextField()),
                ('approved_comment', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('comentariosp', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='respuestasp', to='tienda.comentariop', verbose_name='comentariop')),
                ('likes', models.ManyToManyField(blank=True, null=True, related_name='comentariop_respuestap', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'respuestap',
                'verbose_name_plural': 'respuestasp',
                'ordering': ['-created'],
            },
        ),
        migrations.AddField(
            model_name='comentariop',
            name='producto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comentariosp', to='tienda.producto', verbose_name='producto'),
        ),
    ]
