# Generated by Django 5.0.3 on 2024-12-16 05:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0130_alter_projectboardstatetransition_from_state_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectboardstatetransition',
            name='card',
        ),
        migrations.RemoveField(
            model_name='projectboardstatetransition',
            name='from_state',
        ),
        migrations.RemoveField(
            model_name='projectboardstatetransition',
            name='to_state',
        ),
        migrations.RemoveField(
            model_name='projectboardstatetransition',
            name='transition_time',
        ),
    ]