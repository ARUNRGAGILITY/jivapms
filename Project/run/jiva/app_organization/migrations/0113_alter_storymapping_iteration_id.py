# Generated by Django 5.0.3 on 2024-12-10 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0112_backlog_persona'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storymapping',
            name='iteration_id',
            field=models.PositiveIntegerField(default=-1),
        ),
    ]
