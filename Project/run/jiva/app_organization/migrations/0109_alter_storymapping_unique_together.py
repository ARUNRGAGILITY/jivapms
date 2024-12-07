# Generated by Django 5.0.3 on 2024-12-07 06:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0108_alter_storymapping_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='storymapping',
            unique_together={('release_id', 'iteration_id', 'activity_id', 'step_id', 'persona_id')},
        ),
    ]