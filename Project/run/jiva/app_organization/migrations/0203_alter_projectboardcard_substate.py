# Generated by Django 5.1.5 on 2025-03-31 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0202_rename_date_projectboardstatetransition_date_field_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectboardcard',
            name='substate',
            field=models.CharField(choices=[('Doing', 'Doing'), ('Done', 'Done'), ('MVP', 'MVP'), ('Persevere', 'Persevere'), ('In-Progress', 'In-Progress'), ('Ready', 'Ready')], default='Doing', max_length=50),
        ),
    ]
