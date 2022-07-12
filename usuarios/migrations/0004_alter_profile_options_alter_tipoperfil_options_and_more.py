# Generated by Django 4.0.3 on 2022-05-04 18:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_tipoperfil_rename_bio_profile_bio_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['-id'], 'verbose_name': 'profile', 'verbose_name_plural': 'profiles'},
        ),
        migrations.AlterModelOptions(
            name='tipoperfil',
            options={'ordering': ['-created'], 'verbose_name': 'tipoperfil', 'verbose_name_plural': 'tipoperfiles'},
        ),
        migrations.AddField(
            model_name='tipoperfil',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tipoperfil',
            name='updated',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]