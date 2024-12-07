# Generated by Django 5.0.3 on 2024-12-07 06:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0106_storymapping_story_name'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='storymapping',
            unique_together={('story_id', 'release_id', 'iteration_id', 'activity_id', 'step_id', 'persona_id')},
        ),
    ]