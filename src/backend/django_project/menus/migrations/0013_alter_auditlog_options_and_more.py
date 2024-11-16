# Generated by Django 5.1.3 on 2024-11-15 07:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0012_alter_menuversion_restaurant'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='auditlog',
            options={'verbose_name': 'Audit Log', 'verbose_name_plural': 'Audit Logs'},
        ),
        migrations.AlterModelOptions(
            name='dietaryrestriction',
            options={'verbose_name': 'Dietary Restriction', 'verbose_name_plural': 'Dietary Restrictions'},
        ),
        migrations.AlterModelOptions(
            name='menu',
            options={'verbose_name': 'Menu', 'verbose_name_plural': 'Menus'},
        ),
        migrations.AlterModelOptions(
            name='menuitem',
            options={'verbose_name': 'Menu Item', 'verbose_name_plural': 'Menu Items'},
        ),
        migrations.AlterModelOptions(
            name='menusection',
            options={'verbose_name': 'Menu Section', 'verbose_name_plural': 'Menu Sections'},
        ),
        migrations.AlterModelOptions(
            name='menuversion',
            options={'verbose_name': 'Menu Version', 'verbose_name_plural': 'Menu Versions'},
        ),
        migrations.AlterModelOptions(
            name='openinghours',
            options={'verbose_name': 'Opening Hours', 'verbose_name_plural': 'Opening Hours'},
        ),
        migrations.AlterModelOptions(
            name='restaurant',
            options={'verbose_name': 'Restaurant', 'verbose_name_plural': 'Restaurants'},
        ),
    ]