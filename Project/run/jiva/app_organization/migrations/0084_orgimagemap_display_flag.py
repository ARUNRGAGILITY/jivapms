# Generated by Django 5.0.3 on 2024-11-27 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0083_blog_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='orgimagemap',
            name='display_flag',
            field=models.BooleanField(default=False),
        ),
    ]