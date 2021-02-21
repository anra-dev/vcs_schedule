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
        return reverse('event_detail', kwargs={'pk': self.pk})

    def get_redirect_url_for_event_list(self):
        return self.get_absolute_url()

    class Meta:
        ordering = ['date']
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'


class Conference(models.Model):

    MESSAGES = {
        'create': 'Видеоконференция создана!',
        'update': 'Видеоконференция изменена!',
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
    created_at = models.DateTimeField(auto_now=True)
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

    def __str__(self):
        return f'Конференция "{self.application}" запланирована на {self.date} с {self.time_start} по {self.time_end}'

    @staticmethod
    def get_absolute_url():
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
    created_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=100,
        verbose_name='Статус бронирования',
        choices=STATUS_CHOICES,
        default=STATUS_WAIT
    )

    def __str__(self):
        return f'[Помещение "{self.room}" забронировано на {self.date} с {self.time_start} по {self.time_end}'

    @staticmethod
    def get_absolute_url():
        return reverse('booking_list')

    def get_redirect_url_for_event_list(self):
        return reverse('event_detail', kwargs={'pk': self.event.pk})

    class Meta:
        ordering = ['date', 'time_start']
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'


class Organization(models.Model):

    name = models.CharField(max_length=255, verbose_name='Название организации')
    responsible = models.ForeignKey('Staffer', verbose_name='Ответственный сотрудник', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'


class Room(models.Model):

    address = models.CharField(max_length=255, verbose_name='Адрес')
    room = models.CharField(max_length=255, verbose_name='Комната')
    quota = models.PositiveIntegerField(verbose_name='Вместимость')
    responsible = models.ForeignKey('Staffer', verbose_name='Ответственный сотрудник', on_delete=models.CASCADE)
    applications = models.ManyToManyField('Application', verbose_name='Приложения', related_name='related_room')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.address} {self.room}'

    class Meta:
        ordering = ['address']
        verbose_name = 'Помещение'
        verbose_name_plural = 'Помещения'


class Application(models.Model):

    name = models.CharField(max_length=255, verbose_name='Название приложения')
    server_name = models.CharField(max_length=50, verbose_name='Имя сервера')
    quota = models.PositiveSmallIntegerField(verbose_name='Количество лицензий')
    responsible = models.ForeignKey('Staffer', verbose_name='Ответственный сотрудник', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name } - {self.server_name}'

    class Meta:
        ordering = ['name']
        verbose_name = 'Приложение'
        verbose_name_plural = 'Приложения'


class Staffer(models.Model):

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)  # Потом переделать на OneToOneField on_delete = models.PROTECT
    name = models.CharField(max_length=255, verbose_name='ФИО')
    email = models.EmailField(verbose_name='Электронная почта')
    phone = models.CharField(max_length=100, verbose_name='Телефон')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


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

    event = models.ForeignKey('Event', verbose_name='Мероприятие', null=True, blank=True, on_delete=models.CASCADE)
    created_by = models.ForeignKey('Staffer', verbose_name='Сотрудник', on_delete=models.CASCADE)
    grade = models.SmallIntegerField(verbose_name='Оценка', choices=GRADE_CHOICES)
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Оценку {self.grade} балов поставил(а) {self.created_by}'

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'

