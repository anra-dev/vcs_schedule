# Generated by Django 3.1.7 on 2021-03-13 07:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.SmallIntegerField(unique=True, verbose_name='Порядковый номер')),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'Раздел',
                'verbose_name_plural': 'Разделы',
                'ordering': ['serial_number'],
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.SmallIntegerField(verbose_name='Порядковый номер')),
                ('name', models.CharField(max_length=20, verbose_name='Название')),
                ('slug', models.SlugField(unique=True)),
                ('update_date', models.DateTimeField(verbose_name='Дата изменения')),
                ('title', models.CharField(max_length=60, verbose_name='Заголовок')),
                ('body_text', models.TextField(verbose_name='Содержание страницы')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='help.section', verbose_name='Раздел')),
            ],
            options={
                'verbose_name': 'Страница',
                'verbose_name_plural': 'Страницы',
                'ordering': ['serial_number'],
            },
        ),
    ]