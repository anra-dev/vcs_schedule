from django.db import models
from django.urls import reverse


class Section(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def get_page_list(self):
        return Page.objects.filter(section=self)

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'


class Page(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=60)
    slug = models.SlugField(unique=True)
    section = models.ForeignKey('Section', verbose_name='Раздел', on_delete=models.CASCADE)
    update_date = models.DateTimeField(verbose_name='Дата изменения')
    body_text = models.TextField(verbose_name='Содержание страницы', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'

    def get_absolute_url(self):
        return reverse('help_page', kwargs={'slug': self.slug})
