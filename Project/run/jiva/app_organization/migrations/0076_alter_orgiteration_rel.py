# Generated by Django 5.0.3 on 2024-11-26 07:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0075_orgiteration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orgiteration',
            name='rel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='org_rel_iterations', to='app_organization.orgrelease'),
        ),
    ]