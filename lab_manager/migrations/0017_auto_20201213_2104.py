# Generated by Django 3.1 on 2020-12-13 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lab_manager', '0016_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='print_hours',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
