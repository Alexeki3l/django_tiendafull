# Generated by Django 3.2 on 2023-06-04 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0015_remove_profile_imagen'),
        ('tienda', '0011_auto_20230604_1258'),
        ('multimedia', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='multimedia',
            name='products',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tienda.product'),
        ),
        migrations.AlterField(
            model_name='multimedia',
            name='profiles',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuarios.profile'),
        ),
        migrations.AlterField(
            model_name='multimedia',
            name='stores',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tienda.store'),
        ),
    ]