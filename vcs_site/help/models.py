from django.db import models
from django.urls import reverse


class Section(models.Model):
    serial_number = models.SmallIntegerField(verbose_name='Порядковый номер', unique=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def get_page_list(self):
        return Page.objects.filter(section=self)

    class Meta:
        ordering = ['serial_number']
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'


class Page(models.Model):
    serial_number = models.SmallIntegerField(verbose_name='Порядковый номер')
    name = models.CharField(verbose_name='Название', max_length=20)
    slug = models.SlugField(unique=True)
    section = models.ForeignKey('Section', verbose_name='Раздел', on_delete=models.CASCADE)
    update_date = models.DateTimeField(verbose_name='Дата изменения')
    title = models.CharField(verbose_name='Заголовок', max_length=60)
    body_text = models.TextField(verbose_name='Содержание страницы')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['serial_number']
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'

    def get_absolute_url(self):
        return reverse('help_page', kwargs={'slug': self.slug})
