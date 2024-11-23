# Generated by Django 5.0.3 on 2024-11-23 04:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0059_backlog_iteration_backlog_release'),
    ]

    operations = [
        migrations.AddField(
            model_name='iteration',
            name='release',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='release_iterations', to='app_organization.release'),
        ),
    ]