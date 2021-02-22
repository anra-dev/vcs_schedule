# Generated by Django 3.1.6 on 2021-02-21 22:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0007_auto_20210221_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='conference',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='schedule.conference', verbose_name='Конференция'),
        ),
        migrations.AddField(
            model_name='booking',
            name='without_conference',
            field=models.BooleanField(default=True, verbose_name='Без конференции'),
        ),
    ]
