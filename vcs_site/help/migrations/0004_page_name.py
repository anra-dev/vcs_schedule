# Generated by Django 3.1.6 on 2021-03-06 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('help', '0003_page_section'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='name',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Заголовок'),
        ),
    ]