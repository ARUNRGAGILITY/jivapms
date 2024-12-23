# Generated by Django 5.0.3 on 2024-12-04 14:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0099_remove_impactmapping_node_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImpactMap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('position', models.PositiveIntegerField(default=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('deleted', models.BooleanField(default=False)),
                ('blocked', models.BooleanField(default=False)),
                ('blocked_count', models.PositiveIntegerField(default=0)),
                ('done', models.BooleanField(default=False)),
                ('done_at', models.DateTimeField(blank=True, null=True)),
                ('approved', models.BooleanField(default=False)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('actual_start_date', models.DateTimeField(blank=True, null=True)),
                ('actual_end_date', models.DateTimeField(blank=True, null=True)),
                ('est_duration', models.PositiveIntegerField(default=0)),
                ('total_duration', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(max_length=255)),
                ('node_type', models.CharField(choices=[('Goal', 'Goal'), ('Actor', 'Actor'), ('Impact', 'Impact'), ('Deliverable', 'Deliverable'), ('Task', 'Task')], max_length=20)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='app_organization.impactmap')),
            ],
            options={
                'ordering': ['position'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='impactmapping',
            name='impact_map',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='impact_map', to='app_organization.impactmap'),
        ),
    ]
