# Generated by Django 4.0.3 on 2022-04-19 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_comentario_post_alter_respuesta_comentarios'),
    ]

    operations = [
        migrations.AlterField(
            model_name='respuesta',
            name='comentarios',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='respuestas', to='blog.comentario', verbose_name='comentario'),
        ),
    ]
