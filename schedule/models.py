from datetime import datetime

from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.shortcuts import _get_queryset

from schedule.enums import StatusEnum, ServerTypeEnum, GradeEnum


def get_object_or_none(klass, *args, **kwargs):
    """
    Uses get() to return an object or None if the object does not exist.
    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.
    Note: Like with get(), a MultipleObjectsReturned will be raised if
    more than one object is found.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None


class User(AbstractUser):
    organization = models.ForeignKey(
        'Organization',
        verbose_name='Организация',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    phone = models.CharField(
        verbose_name='Телефон',
        max_length=100,
        null=True,
        blank=True,
    )
    telegram = models.CharField(
        verbose_name='Телеграм чат-id',
        max_length=10,
        null=True,
        blank=True,
    )
    subscribe_telegram = models.BooleanField(
        verbose_name='Подписка на рассылку в телеграм',
        default=False,
    )
    subscribe_mail = models.BooleanField(
        verbose_name='Подписка на почтовую рассылку',
        default=False,
    )
    is_operator = models.BooleanField(
        verbose_name='Оператор',
        default=False,
    )
    is_assistant = models.BooleanField(
        verbose_name='Ассистент',
        default=False,
    )

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class EventManager(models.Manager):
    """
    Менеджер, который списывает мероприятия в архив.

    Данная реализация потенциально вызывает много запросов. На данный
    момент некритично, но в дальнейшем лучше переделать.
    """
    def get_queryset(self):
        now = datetime.now()
        current_date = now.date()
        current_time = now.time()
        super().get_queryset().filter(
            Q(date__lt=current_date) |
            Q(date=current_date, time_end__lt=current_time),
        ).update(
            status=StatusEnum.STATUS_COMPLETED,
            conf_status=StatusEnum.STATUS_COMPLETED,
            booking_status=StatusEnum.STATUS_COMPLETED,
        )
        return super().get_queryset()


class Event(models.Model):
    objects = EventManager()

    name = models.CharField(
        verbose_name='Название мероприятия',
        max_length=255,
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    # Организация - возможно избыточно
    organization = models.ForeignKey(
        'Organization',
        verbose_name='Организация',
        on_delete=models.CASCADE,
    )
    owner = models.ForeignKey(
        'User',
        verbose_name='Владелец',
        on_delete=models.CASCADE,
    )
    date = models.DateField(
        verbose_name='Дата',
    )
    time_start = models.TimeField(
        verbose_name='Время начала',
    )
    time_end = models.TimeField(
        verbose_name='Время окончания',
    )
    status = models.PositiveSmallIntegerField(
        verbose_name='Статус мероприятия',
        choices=StatusEnum.choices,
        default=StatusEnum.STATUS_DRAFT,
    )
    # VCS
    with_conf = models.BooleanField(
        verbose_name='Нужна видеоконференция',
        default=False,
    )
    conf_operator = models.ForeignKey(
        'User',
        verbose_name='Оператор',
        related_name='event_conference_operator',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    conf_server = models.ForeignKey(
        'Server',
        verbose_name='Сервер',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    conf_note = models.TextField(
        verbose_name='Примечание',
        null=True,
        blank=True,
    )
    conf_number_clients = models.PositiveSmallIntegerField(
        verbose_name='Количество участников',
        null=True,
        blank=True,
    )
    conf_file = models.FileField(
        verbose_name='Файл',
        upload_to='uploads/%Y/%m/%d/',
        null=True,
        blank=True,
    )
    conf_link = models.CharField(
        max_length=255,
        verbose_name='Ссылка',
        null=True,
        blank=True,
    )
    conf_status = models.PositiveSmallIntegerField(
        verbose_name='Статус видеоконференции',
        choices=StatusEnum.choices,
        default=StatusEnum.STATUS_DRAFT,
        null=True,
        blank=True,
    )
    conf_reason = models.TextField(
        verbose_name='Причина отказа',
        null=True,
        blank=True,
    )
    # Booking
    with_booking = models.BooleanField(
        verbose_name='Нужно помещение',
        default=False,
    )
    booking_assistant = models.ForeignKey(
        'User',
        verbose_name='Ассистент',
        on_delete=models.PROTECT,
        related_name='event_booking_assistant',
        null=True,
        blank=True,
    )
    booking_room = models.ForeignKey(
        'Room',
        verbose_name='Место проведения',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    booking_note = models.TextField(
        verbose_name='Примечание',
        null=True,
        blank=True,
    )
    booking_status = models.PositiveSmallIntegerField(
        verbose_name='Статус бронирования',
        choices=StatusEnum.choices,
        default=StatusEnum.STATUS_DRAFT,
        null=True,
        blank=True,
    )
    booking_reason = models.TextField(
        verbose_name='Причина отказа',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f'Мероприятие "{self.name}" на {self.date}'

    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['date', 'time_start']
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'


class Room(models.Model):

    address = models.CharField(
        verbose_name='Адрес',
        max_length=255,
    )
    room = models.CharField(
        verbose_name='Комната',
        max_length=255,
    )
    quota = models.PositiveIntegerField(
        verbose_name='Вместимость',
    )
    assistants = models.ManyToManyField(
        'User',
        verbose_name='Ассистенты',
    )
    server = models.ManyToManyField(
        'Server',
        verbose_name='Доступные серверы',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f'{self.address} {self.room} на {self.quota} человек(а)'

    class Meta:
        ordering = ['address']
        verbose_name = 'Помещение'
        verbose_name_plural = 'Помещения'


class Server(models.Model):

    name = models.CharField(
        max_length=255,
        verbose_name='Название сервера',
    )
    application = models.ForeignKey(
        'Application',
        verbose_name='Приложение',
        on_delete=models.CASCADE,
    )
    server_address = models.CharField(
        max_length=50,
        verbose_name='Адрес сервера',
        null=True,
        blank=True,
    )
    quota = models.PositiveSmallIntegerField(
        verbose_name='Количество лицензий',
    )
    operators = models.ManyToManyField(
        'User',
        verbose_name='Операторы',
    )
    type = models.PositiveSmallIntegerField(
        verbose_name='Тип сервера',
        choices=ServerTypeEnum.choices,
        default=ServerTypeEnum.SERVER_TYPE_EXTERNAL,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        if self.application:
            return f'{self.name } - {self.application}'
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Сервер'
        verbose_name_plural = 'Сервера'


class Organization(models.Model):

    name = models.CharField(
        verbose_name='Название организации',
        max_length=255,
    )
    room = models.ManyToManyField(
        'Room',
        verbose_name='Доступные помещения',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'


class Application(models.Model):

    name = models.CharField(
        max_length=255,
        verbose_name='Название приложения',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Приложение'
        verbose_name_plural = 'Приложения'


class Grade(models.Model):

    event = models.ForeignKey(
        'Event',
        verbose_name='Мероприятие',
        on_delete=models.CASCADE,
    )
    created_by = models.ForeignKey(
        'User',
        verbose_name='Сотрудник',
        on_delete=models.CASCADE,
    )
    grade = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        choices=GradeEnum.choices,
    )
    comment = models.TextField(
        verbose_name='Комментарий',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f'Оценку {self.grade} балов поставил(а) {self.created_by}'

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'


@receiver(pre_save, sender=Event)
def update_status_event(instance, **kwargs):
    """
    Обновляет статус мероприятия
    """
    from dispatch.calling import send_out_message

    statuses = {instance.conf_status, instance.booking_status}
    if len(statuses) == 0:
        instance.status = StatusEnum.STATUS_DRAFT
    elif len(statuses) == 1:
        same_status = statuses.pop()
        if same_status == StatusEnum.STATUS_READY:
            send_out_message(instance)
        instance.status = same_status
    else:
        if StatusEnum.STATUS_WAIT in statuses:
            instance.status = StatusEnum.STATUS_WAIT
        if StatusEnum.STATUS_REJECTION in statuses:
            instance.status = StatusEnum.STATUS_REJECTION
