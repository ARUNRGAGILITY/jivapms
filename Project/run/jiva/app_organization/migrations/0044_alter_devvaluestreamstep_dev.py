# Generated by Django 5.0.3 on 2024-11-17 05:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0043_devvaluestream_trigger_devvaluestream_value_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devvaluestreamstep',
            name='dev',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dev_value_stream_steps', to='app_organization.devvaluestream'),
        ),
    ]
