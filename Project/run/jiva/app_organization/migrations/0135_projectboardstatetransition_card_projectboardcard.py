# Generated by Django 5.0.3 on 2024-12-16 07:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0134_remove_projectboardstatetransition_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectboardstatetransition',
            name='card',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='card_transitions', to='app_organization.backlog'),
        ),
        migrations.CreateModel(
            name='ProjectBoardCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
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
                ('backlog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='board_cards', to='app_organization.backlog')),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='board_cards', to='app_organization.projectboard')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='state_cards', to='app_organization.projectboardstate')),
            ],
            options={
                'ordering': ['position'],
                'abstract': False,
            },
        ),
    ]