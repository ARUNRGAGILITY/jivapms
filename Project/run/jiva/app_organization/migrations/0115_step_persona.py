# Generated by Django 5.0.3 on 2024-12-11 06:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0114_alter_storymapping_iteration_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='step',
            name='persona',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='persona_steps', to='app_organization.persona'),
        ),
    ]
