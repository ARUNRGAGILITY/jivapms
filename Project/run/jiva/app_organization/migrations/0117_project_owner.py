# Generated by Django 5.0.3 on 2024-12-14 05:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_memberprofilerole', '0003_orgadmin_projectadmin_siteadmin_memberprofilerole'),
        ('app_organization', '0116_alter_backlog_iteration_alter_backlog_release'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owner_projects', to='app_memberprofilerole.member'),
        ),
    ]