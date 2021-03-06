# Generated by Django 3.1.6 on 2021-03-06 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('help', '0004_page_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='page',
            options={'ordering': ['name'], 'verbose_name': 'Страница', 'verbose_name_plural': 'Страницы'},
        ),
        migrations.AlterModelOptions(
            name='section',
            options={'ordering': ['serial_number'], 'verbose_name': 'Раздел', 'verbose_name_plural': 'Разделы'},
        ),
        migrations.AddField(
            model_name='section',
            name='serial_number',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Порядковый номер'),
        ),
        migrations.AlterField(
            model_name='page',
            name='name',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Название'),
        ),
    ]