# Generated by Django 4.0.3 on 2022-04-25 14:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0015_post_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='post_comentario', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='post_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='respuesta',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='comentario_respuesta', to=settings.AUTH_USER_MODEL),
        ),
    ]
