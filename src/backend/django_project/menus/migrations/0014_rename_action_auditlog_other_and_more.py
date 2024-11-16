# Generated by Django 5.1.3 on 2024-11-15 07:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0013_alter_auditlog_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auditlog',
            old_name='action',
            new_name='other',
        ),
        migrations.RenameField(
            model_name='auditlog',
            old_name='entity_affected',
            new_name='phase',
        ),
        migrations.RemoveField(
            model_name='auditlog',
            name='menu',
        ),
        migrations.RemoveField(
            model_name='auditlog',
            name='new_value',
        ),
        migrations.RemoveField(
            model_name='auditlog',
            name='old_value',
        ),
        migrations.AddField(
            model_name='auditlog',
            name='menu_version',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='menus.menuversion'),
        ),
        migrations.AddField(
            model_name='auditlog',
            name='time_registered',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='auditlog',
            name='status',
            field=models.CharField(blank=True, max_length=99, null=True),
        ),
    ]