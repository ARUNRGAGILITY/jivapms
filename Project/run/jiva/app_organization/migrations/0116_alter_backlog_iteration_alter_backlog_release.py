# Generated by Django 5.0.3 on 2024-12-11 17:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0115_step_persona'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backlog',
            name='iteration',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='backlog_iteration', to='app_organization.orgiteration'),
        ),
        migrations.AlterField(
            model_name='backlog',
            name='release',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='backlog_releases', to='app_organization.orgrelease'),
        ),
    ]
