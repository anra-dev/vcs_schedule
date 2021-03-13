from django.db import models
from schedule.models import User


class Message(models.Model):

    recipient = models.ManyToManyField(User, verbose_name='Получатель', blank=True)
    message = models.TextField(verbose_name='Сообщение', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.created_at)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
