from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()


class Event(models.Model):

    MESSAGES = {
        'create': 'Мероприятие создано!',
        'edit': 'Мероприятие изменено!',
        'delete': 'Мероприятие удалено!'
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

    name = models.CharField(max_length=255, verbose_name='Название мероприятия')
    description = models.TextField(verbose_name='Описание')
    organization = models.ForeignKey('Organization', verbose_name='Организация', on_delete=models.CASCADE)
    responsible = models.ForeignKey('Staffer', verbose_name='Ответственный сотрудник', on_delete=models.CASCADE)
    date = models.DateField(verbose_name='Дата проведения')
    created_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=100,
        verbose_name='Статус мероприятия',
        choices=STATUS_CHOICES,
        default=STATUS_WAIT
    )

    def __str__(self):
        return f'Мероприятие "{self.name}" запланировано на {self.date}'

    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'event_id': self.id})

    def get_redirect_url_for_event_list(self):
        return reverse('event_detail', kwargs={'event_id': self.id})

    class Meta:
        ordering = ['-date']


class Conference(models.Model):

    MESSAGES = {
        'create': 'Видеоконференция создана!',
        'edit': 'Видеоконференция изменена!',
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

    EVENT_TYPE_EXTERNAL = 'external'
    EVENT_TYPE_LOCAL = 'local'

    EVENT_TYPE_CHOICES = (
        (EVENT_TYPE_EXTERNAL, 'Внешний'),
        (EVENT_TYPE_LOCAL, 'Внутренний')
    )

    event = models.ForeignKey('Event', verbose_name='Мероприятие', null=True, blank=True, on_delete=models.CASCADE)
    application = models.ForeignKey('Application', verbose_name='Приложение', on_delete=models.CASCADE)

    quota = models.PositiveSmallIntegerField(verbose_name='Количество участников', null=True, blank=True)
    link_to_event = models.CharField(max_length=255, verbose_name='Ссылка', null=True, blank=True)
    date = models.DateField(verbose_name='Дата проведения')
    time_start = models.TimeField(verbose_name='Время начала')
    time_end = models.TimeField(verbose_name='Время окончания')
    type = models.CharField(
        max_length=100,
        verbose_name='Тип видеоконференции',
        choices=EVENT_TYPE_CHOICES,
        default=EVENT_TYPE_LOCAL
    )
    status = models.CharField(
        max_length=100,
        verbose_name='Статус видеоконференции',
        choices=STATUS_CHOICES,
        default=STATUS_WAIT
    )

    def get_absolute_url(self):
        return reverse('conference_list')

    def get_redirect_url_for_event_list(self):
        return reverse('event_detail', kwargs={'event_id': self.event.id})

    class Meta:
        ordering = ['-date']


class Booking(models.Model):

    MESSAGES = {
        'create': 'Бронирование создано!',
        'edit': 'Бронирование изменено!',
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

    event = models.ForeignKey('Event', verbose_name='Мероприятие', null=True, blank=True, on_delete=models.CASCADE)
    room = models.ForeignKey('Room', verbose_name='Место проведения', null=True, blank=True, on_delete=models.CASCADE)
    quota = models.PositiveSmallIntegerField(verbose_name='Количество участников')
    date = models.DateField(verbose_name='Дата проведения')
    time_start = models.TimeField(verbose_name='Время начала')
    time_end = models.TimeField(verbose_name='Время окончания')
    status = models.CharField(
        max_length=100,
        verbose_name='Статус бронирования',
        choices=STATUS_CHOICES,
        default=STATUS_WAIT
    )

    def get_redirect_url_for_event_list(self):
        return reverse('event_detail', kwargs={'event_id': self.event.id})

    class Meta:
        ordering = ['-date']


class Organization(models.Model):

    name = models.CharField(max_length=255, verbose_name='Название организации')
    responsible = models.ForeignKey('Staffer', verbose_name='Ответственный сотрудник', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Room(models.Model):

    address = models.CharField(max_length=255, verbose_name='Адрес')
    room = models.CharField(max_length=255, verbose_name='Комната')
    quota = models.PositiveIntegerField(verbose_name='Вместимость')
    responsible = models.ForeignKey('Staffer', verbose_name='Ответственный сотрудник', on_delete=models.CASCADE)
    applications = models.ManyToManyField('Application', verbose_name='Приложения', related_name='related_room')

    def __str__(self):
        return f'{self.address} {self.room}'


class Application(models.Model):

    name = models.CharField(max_length=255, verbose_name='Название приложения')
    server_name = models.CharField(max_length=50, verbose_name='Имя сервера')
    quota = models.PositiveSmallIntegerField(verbose_name='Количество лицензий')
    responsible = models.ForeignKey('Staffer', verbose_name='Ответственный сотрудник', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Staffer(models.Model):

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name='ФИО')
    email = models.EmailField(verbose_name='Электронная почта')
    phone = models.CharField(max_length=100, verbose_name='Телефон')

    def __str__(self):
        return self.name
