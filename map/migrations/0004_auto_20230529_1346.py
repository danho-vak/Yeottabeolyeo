# Generated by Django 3.2 on 2023-05-29 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0003_auto_20230529_1343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='box',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='box',
            name='longitude',
        ),
    ]