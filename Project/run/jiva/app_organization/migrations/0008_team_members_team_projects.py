# Generated by Django 5.0.3 on 2024-10-08 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_memberprofilerole', '0001_initial'),
        ('app_organization', '0007_alter_projectrole_role_type_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(related_name='teams', to='app_memberprofilerole.member'),
        ),
        migrations.AddField(
            model_name='team',
            name='projects',
            field=models.ManyToManyField(related_name='teams', to='app_organization.project'),
        ),
    ]