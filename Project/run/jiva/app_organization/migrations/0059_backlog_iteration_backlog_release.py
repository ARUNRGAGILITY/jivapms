# Generated by Django 5.0.3 on 2024-11-23 04:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0058_imagemap_original_height_imagemap_original_width'),
    ]

    operations = [
        migrations.AddField(
            model_name='backlog',
            name='iteration',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='backlog_iteration', to='app_organization.iteration'),
        ),
        migrations.AddField(
            model_name='backlog',
            name='release',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='backlog_releases', to='app_organization.release'),
        ),
    ]
