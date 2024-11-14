# Generated by Django 5.1.3 on 2024-11-14 19:09

import storages.backends.s3
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0006_remove_menu_menupdf_menu_menu_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='menu_file',
            field=models.FileField(blank=True, null=True, storage=storages.backends.s3.S3Storage(), upload_to='menu_files/'),
        ),
    ]