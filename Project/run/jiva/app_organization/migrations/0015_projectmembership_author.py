# Generated by Django 5.0.3 on 2024-10-09 11:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0014_remove_backlog_org_remove_backlogsupertype_org_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='projectmembership',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author_projectmembership', to=settings.AUTH_USER_MODEL),
        ),
    ]