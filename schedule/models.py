from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.shortcuts import _get_queryset

from schedule.enums import StatusEnum, ServerTypeEnum


def get_object_or_none(klass, *args, **kwargs):
    """
    Uses get() to return an object or None if the object does not exist.
    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.
    Note: Like with get(), a MultipleObjectsReturned will be raised if more than one
    object is found.
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


class Event(models.Model):

    MESSAGES = {
        'create': 'Мероприятие создано!',
        'update': 'Мероприятие изменено!',
        'delete': 'Мероприятие удалено!'
    }

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

    def get_avg_grade(self):
        return Grade.objects.filter(
            event=self
        ).aggregate(models.Avg('grade'))['grade__avg']

    def get_grade(self):
        return get_object_or_none(Grade, event=self).grade

    class Meta:
        ordering = ['date', 'time_start']
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'


class Conference(models.Model):

    MESSAGES = {
        'create': 'Видеоконференция создана!',
        'update': 'Видеоконференция изменена!',
        'approve': 'Видеоконференция обработана!',
        'delete': 'Видеоконференция удалена!'
    }

    STATUS_WAIT = 'wait'
    STATUS_READY = 'ready'
    STATUS_REJECTION = 'rejection'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = (
        (STATUS_WAIT, 'Ожидание'),
        (STATUS_READY, 'Готово'),
        (STATUS_REJECTION, 'Отказ'),
        (STATUS_COMPLETED, 'Окончено')
    )

    event = models.OneToOneField(
        'Event',
        verbose_name='Мероприятие',
        on_delete=models.CASCADE,
        primary_key=True,
    )
    server = models.ForeignKey(
        'Server',
        verbose_name='Сервер',
        on_delete=models.CASCADE,
    )
    owner = models.ForeignKey(
        'User',
        verbose_name='Владелец',
        related_name='conference_owner',
        on_delete=models.CASCADE,
    )
    operator = models.ForeignKey(
        'User',
        verbose_name='Оператор',
        related_name='conference_operator',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True,
    )
    file = models.FileField(
        verbose_name='Файл',
        upload_to='uploads/%Y/%m/%d/',
        null=True,
        blank=True,
    )
    quota = models.PositiveSmallIntegerField(
        verbose_name='Количество участников',
        null=True,
        blank=True,
    )
    link = models.CharField(
        max_length=255,
        verbose_name='Ссылка',
        null=True,
        blank=True,
    )
    date = models.DateField(
        verbose_name='Дата проведения',
    )
    time_start = models.TimeField(
        verbose_name='Время начала',
    )
    time_end = models.TimeField(
        verbose_name='Время окончания',
    )
    status = models.CharField(
        max_length=100,
        verbose_name='Статус видеоконференции',
        choices=STATUS_CHOICES,
        default=STATUS_WAIT,
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
        return (f'Конференция на "{self.server}" запланирована '
                f'на {self.date} с {self.time_start} по {self.time_end}')

    @staticmethod
    def get_list_url():
        return reverse('conference_list')

    def get_redirect_url_for_event_list(self):
        return reverse('event_detail', kwargs={'pk': self.event.pk})

    class Meta:
        ordering = ['date', 'time_start']
        verbose_name = 'Конференция'
        verbose_name_plural = 'Конференции'


class Booking(models.Model):

    MESSAGES = {
        'create': 'Бронирование создано!',
        'update': 'Бронирование изменено!',
        'approve': 'Бронирование обработано!',
        'delete': 'Бронирование удалено!'
    }

    STATUS_WAIT = 'wait'
    STATUS_READY = 'ready'
    STATUS_REJECTION = 'rejection'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = (
        (STATUS_WAIT, 'Ожидание'),
        (STATUS_READY, 'Готово'),
        (STATUS_REJECTION, 'Отказ'),
        (STATUS_COMPLETED, 'Окончено')
    )

    event = models.OneToOneField(
        'Event',
        verbose_name='Мероприятие',
        on_delete=models.CASCADE,
        primary_key=True,
    )
    conference = models.ForeignKey(
        'Conference',
        verbose_name='Конференция',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    without_conference = models.BooleanField(
        verbose_name='Без конференции',
        default=False,
    )
    owner = models.ForeignKey(
        'User',
        verbose_name='Владелец',
        on_delete=models.CASCADE,
        related_name='booking_owner',
    )
    assistant = models.ForeignKey(
        'User',
        verbose_name='Ассистент',
        on_delete=models.CASCADE,
        related_name='booking_assistant',
        null=True,
        blank=True,
    )
    room = models.ForeignKey(
        'Room',
        verbose_name='Место проведения',
        on_delete=models.CASCADE,
    )
    quota = models.PositiveSmallIntegerField(
        verbose_name='Количество участников',
    )
    date = models.DateField(
        verbose_name='Дата проведения',
    )
    time_start = models.TimeField(
        verbose_name='Время начала',
    )
    time_end = models.TimeField(
        verbose_name='Время окончания',
    )
    status = models.CharField(
        max_length=100,
        verbose_name='Статус бронирования',
        choices=STATUS_CHOICES,
        default=STATUS_WAIT,
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
        return (f'Помещение "{self.room}" забронировано '
                f'на {self.date} с {self.time_start} по {self.time_end}')

    @staticmethod
    def get_list_url():
        return reverse('booking_list')

    def get_redirect_url_for_event_list(self):
        return reverse('event_detail', kwargs={'pk': self.event.pk})

    class Meta:
        ordering = ['date', 'time_start']
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'


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

    GRADE_1 = 1
    GRADE_2 = 2
    GRADE_3 = 3
    GRADE_4 = 4
    GRADE_5 = 5

    GRADE_CHOICES = (
        (GRADE_1, 'Очень плохо'),
        (GRADE_2, 'Плохо'),
        (GRADE_3, 'Удовлетворительно'),
        (GRADE_4, 'Хорошо'),
        (GRADE_5, 'Отлично')
    )

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
        choices=GRADE_CHOICES,
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
