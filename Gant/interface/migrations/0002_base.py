# Generated by Django 4.0.4 on 2022-07-05 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Base',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail_number', models.IntegerField()),
                ('detail_stanok_number', models.IntegerField()),
                ('detail_time', models.IntegerField()),
            ],
        ),
    ]
