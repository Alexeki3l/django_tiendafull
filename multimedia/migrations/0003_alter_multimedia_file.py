# Generated by Django 3.2 on 2023-06-06 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multimedia', '0002_auto_20230604_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='multimedia',
            name='file',
            field=models.FileField(default='/media/store/sin-photo.jpg', upload_to=''),
        ),
    ]