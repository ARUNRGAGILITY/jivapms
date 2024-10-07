# Generated by Django 5.0.3 on 2024-10-07 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0004_remove_projectrole_project_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectrole',
            name='role_type',
            field=models.CharField(choices=[('admin', 'Admin'), ('editor', 'Editor'), ('viewer', 'Viewer'), ('no_view', 'No View')], default='no_view', max_length=255),
        ),
    ]
