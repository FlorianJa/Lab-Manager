# Generated by Django 3.1 on 2020-12-04 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lab_manager', '0008_auto_20201204_0507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fablabuser',
            name='last_access_date',
            field=models.CharField(default='', max_length=14),
        ),
    ]