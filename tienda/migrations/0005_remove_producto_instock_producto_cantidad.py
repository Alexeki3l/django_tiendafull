# Generated by Django 4.0.3 on 2022-05-02 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0004_rename_tiendas_producto_tienda'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='instock',
        ),
        migrations.AddField(
            model_name='producto',
            name='cantidad',
            field=models.IntegerField(default=12),
            preserve_default=False,
        ),
    ]
