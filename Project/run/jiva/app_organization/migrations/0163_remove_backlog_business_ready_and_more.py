# Generated by Django 5.0.3 on 2024-12-26 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0162_backlog_business_ready_backlog_ops_ready_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='backlog',
            name='business_ready',
        ),
        migrations.RemoveField(
            model_name='backlog',
            name='ops_ready',
        ),
        migrations.RemoveField(
            model_name='backlog',
            name='tech_ready',
        ),
    ]
