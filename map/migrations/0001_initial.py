# Generated by Django 3.2 on 2023-05-29 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Box',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('district', models.CharField(max_length=50, verbose_name='행정구역')),
                ('address', models.CharField(max_length=100, verbose_name='주소')),
                ('address_detail', models.CharField(blank=True, max_length=200, null=True, verbose_name='상세주소')),
                ('latitude', models.FloatField(verbose_name='위도')),
                ('longitude', models.FloatField(verbose_name='경도')),
                ('type', models.CharField(choices=[('의류수거함', '의류수거함'), ('건전지수거함', '건전지수거함'), ('형광등수거함', '형광등수거함')], max_length=50, verbose_name='수거함타입')),
            ],
            options={
                'verbose_name': '수거함',
            },
        ),
    ]
