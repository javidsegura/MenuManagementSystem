# Generated by Django 5.1.3 on 2024-11-14 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0007_alter_menu_menu_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='menu_file',
            field=models.FileField(blank=True, null=True, upload_to='menu_files/'),
        ),
    ]
