# Generated by Django 5.0.3 on 2024-11-26 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0079_remove_orgiteration_rel_orgiteration_org_release'),
    ]

    operations = [
        migrations.AddField(
            model_name='orgrelease',
            name='planning_buffer',
            field=models.PositiveIntegerField(default=2),
        ),
    ]
