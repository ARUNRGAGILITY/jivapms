# Generated by Django 5.1.5 on 2025-03-31 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0203_alter_projectboardcard_substate'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectboardstate',
            name='subcolumn_pair',
            field=models.CharField(blank=True, choices=[('DOING_DONE', 'Doing / Done'), ('INPROGRESS_READY', 'In Progress / Ready'), ('MVP_PERSEVERE', 'MVP / Persevere')], help_text='Applicable only when buffer_column is True', max_length=30, null=True),
        ),
    ]
