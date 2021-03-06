# Generated by Django 3.1.6 on 2021-03-06 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('help', '0005_auto_20210306_1454'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='page',
            options={'ordering': ['serial_number'], 'verbose_name': 'Страница', 'verbose_name_plural': 'Страницы'},
        ),
        migrations.AddField(
            model_name='page',
            name='serial_number',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Порядковый номер'),
        ),
    ]