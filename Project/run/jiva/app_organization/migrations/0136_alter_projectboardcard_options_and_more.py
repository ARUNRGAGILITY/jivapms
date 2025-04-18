# Generated by Django 5.0.3 on 2024-12-16 08:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0135_projectboardstatetransition_card_projectboardcard'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectboardcard',
            options={},
        ),
        migrations.AddField(
            model_name='projectboardcard',
            name='swimlane',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='swimlane_cards', to='app_organization.projectboardswimlane'),
        ),
        migrations.AddField(
            model_name='projectboardstatetransition',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='projectboardstatetransition',
            name='triggered_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='projectboardcard',
            index=models.Index(fields=['board', 'state'], name='app_organiz_board_i_a7cad0_idx'),
        ),
    ]
