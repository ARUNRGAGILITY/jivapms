# Generated by Django 5.1.5 on 2025-04-07 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_memberprofilerole', '0005_alter_profile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='name',
        ),
    ]
