# Generated by Django 5.0.3 on 2024-10-09 08:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0012_teammember_member_role'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BacklogSuperType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('text', models.TextField(blank=True, null=True)),
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
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author_backlog_super_typesupertypes', to=settings.AUTH_USER_MODEL)),
                ('org', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='backlog_super_type_supertypes', to='app_organization.organization')),
            ],
            options={
                'ordering': ['position'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BacklogType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('text', models.TextField(blank=True, null=True)),
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
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author_backlogtypes', to=settings.AUTH_USER_MODEL)),
                ('org', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='backlog_type_types', to='app_organization.organization')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supertype', to='app_organization.backlogtype')),
                ('super_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supertype_backlogtypes', to='app_organization.backlogsupertype')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_backlogtypes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Backlog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('text', models.TextField(blank=True, null=True)),
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
                ('tag', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('duration_in_hours', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author_backlogs', to=settings.AUTH_USER_MODEL)),
                ('org', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='backlogs', to='app_organization.organization')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Organization', to='app_organization.backlog')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_backlogs', to=settings.AUTH_USER_MODEL)),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='backlog_types', to='app_organization.backlogtype')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]