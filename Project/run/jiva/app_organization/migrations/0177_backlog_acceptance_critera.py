# Generated by Django 5.1.5 on 2025-02-14 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0176_alter_projectdetail_pro'),
    ]

    operations = [
        migrations.AddField(
            model_name='backlog',
            name='acceptance_critera',
            field=models.TextField(blank=True, null=True),
        ),
    ]
