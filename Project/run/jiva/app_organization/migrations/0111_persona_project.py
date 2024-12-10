# Generated by Django 5.0.3 on 2024-12-09 18:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0110_alter_storymapping_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_personae', to='app_organization.project'),
        ),
    ]
