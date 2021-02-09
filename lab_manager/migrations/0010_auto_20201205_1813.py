# Generated by Django 3.1 on 2020-12-05 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lab_manager', '0009_auto_20201204_0515'),
    ]

    operations = [
        migrations.AddField(
            model_name='fablabuser',
            name='assigned_by',
            field=models.CharField(default='admin', max_length=14),
        ),
        migrations.AlterField(
            model_name='fablabuser',
            name='printer_name',
            field=models.CharField(max_length=14, unique=True),
        ),
    ]