# Generated by Django 4.0.4 on 2022-08-18 19:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sessions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vocabulary',
            fields=[
                ('series', models.IntegerField(blank=True, null=True)),
                ('methods', models.TextField(blank=True, null=True)),
                ('details', models.IntegerField(blank=True, null=True)),
                ('tools', models.IntegerField(blank=True, null=True)),
                ('redis', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='sessions.session')),
            ],
        ),
        migrations.CreateModel(
            name='Base',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail_number', models.IntegerField()),
                ('detail_stanok_number', models.IntegerField()),
                ('detail_time', models.IntegerField()),
                ('detail_turn', models.IntegerField(blank=True, null=True)),
                ('redis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sessions.session')),
            ],
            options={
                'verbose_name': 'Деталь',
                'verbose_name_plural': 'Детали',
            },
        ),
    ]
