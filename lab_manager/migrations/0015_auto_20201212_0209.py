# Generated by Django 3.1 on 2020-12-12 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lab_manager', '0014_auto_20201210_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='operating',
            name='printer_name',
            field=models.CharField(default='Other', max_length=14, unique=True),
        ),
        migrations.AddField(
            model_name='printer',
            name='printer_name',
            field=models.CharField(default='Other', max_length=14, unique=True),
        ),
    ]