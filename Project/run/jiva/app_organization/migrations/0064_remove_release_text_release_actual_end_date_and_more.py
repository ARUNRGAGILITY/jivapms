# Generated by Django 5.0.3 on 2024-11-24 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0063_iteration_iteration_length'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='release',
            name='text',
        ),
        migrations.AddField(
            model_name='release',
            name='actual_end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='release',
            name='actual_start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='release',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='release',
            name='est_duration',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='release',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='release',
            name='total_duration',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
