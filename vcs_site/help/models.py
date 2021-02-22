from django.db import models
from django.urls import reverse


class Page(models.Model):
    title = models.CharField(max_length=60)
    slug = models.SlugField(unique=True)
    update_date = models.DateTimeField('Last Updated')
    body_text = models.TextField('Page content', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'

    def get_absolute_url(self):
        return reverse('help_page', kwargs={'slug': self.slug})
