# Generated by Django 5.0.3 on 2024-12-25 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0157_orgiteration_build_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='orgiteration',
            name='hotfix',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]