# Generated by Django 5.1.3 on 2024-11-14 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0005_alter_menu_active_status_alter_menu_available_from_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='menuPdf',
        ),
        migrations.AddField(
            model_name='menu',
            name='menu_file',
            field=models.FileField(blank=True, null=True, upload_to='menu_files/'),
        ),
    ]