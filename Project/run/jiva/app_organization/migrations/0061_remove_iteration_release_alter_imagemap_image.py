# Generated by Django 5.0.3 on 2024-11-23 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0060_iteration_release'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='iteration',
            name='release',
        ),
        migrations.AlterField(
            model_name='imagemap',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='folder_image_maps/'),
        ),
    ]