# Generated by Django 5.0.3 on 2024-10-07 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0005_alter_projectrole_role_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectrole',
            name='test_field',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
