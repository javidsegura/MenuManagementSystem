# Generated by Django 5.1.3 on 2024-11-15 07:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0011_remove_menuversion_post_alter_menuversion_restaurant_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuversion',
            name='restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='menus.restaurant'),
        ),
    ]