# Generated by Django 5.0.3 on 2024-12-04 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0100_impactmap_impactmapping_impact_map'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impactmap',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='impactmap',
            name='node_type',
            field=models.CharField(choices=[('Goal', 'Goal'), ('Actor', 'Actor'), ('Impact', 'Impact'), ('Deliverable', 'Deliverable'), ('Task', 'Task')], default=None, max_length=20),
        ),
    ]