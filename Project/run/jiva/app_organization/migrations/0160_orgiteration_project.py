# Generated by Django 5.0.3 on 2024-12-25 09:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0159_orgrelease_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='orgiteration',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_org_iterations', to='app_organization.project'),
        ),
    ]