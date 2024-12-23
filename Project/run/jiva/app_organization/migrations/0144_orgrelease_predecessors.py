# Generated by Django 5.0.3 on 2024-12-23 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0143_orgrelease_no_of_iterations'),
    ]

    operations = [
        migrations.AddField(
            model_name='orgrelease',
            name='predecessors',
            field=models.ManyToManyField(blank=True, related_name='successors', to='app_organization.orgrelease'),
        ),
    ]
