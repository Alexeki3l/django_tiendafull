# Generated by Django 4.0.3 on 2022-04-26 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_alter_comentario_likes_alter_post_likes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='approved_post',
            field=models.BooleanField(default=True),
        ),
    ]