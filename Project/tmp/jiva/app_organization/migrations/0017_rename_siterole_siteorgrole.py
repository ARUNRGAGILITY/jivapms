# Generated by Django 5.0.3 on 2024-10-09 14:56

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0016_siterole_sitemembership'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SiteRole',
            new_name='Siteorgrole',
        ),
    ]