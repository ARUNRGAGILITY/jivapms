# Generated by Django 5.0.3 on 2024-12-04 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0098_impactmapping_node_type_impactmapping_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='impactmapping',
            name='node_type',
        ),
        migrations.RemoveField(
            model_name='impactmapping',
            name='parent',
        ),
    ]
