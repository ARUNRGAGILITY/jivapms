# Generated by Django 5.0.3 on 2024-11-16 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0041_devvaluestreamstep_supporting_ops_steps'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devvaluestreamstep',
            name='supporting_ops_steps',
        ),
        migrations.AddField(
            model_name='devvaluestream',
            name='supporting_ops_steps',
            field=models.ManyToManyField(blank=True, related_name='supported_by_dev_steps', to='app_organization.opsvaluestreamstep'),
        ),
    ]
