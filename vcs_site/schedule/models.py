from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()


class Event(models.Model):

    MESSAGES = {
        'create': 'Мероприятие создано!',
        'update': 'Мероприятие изменено!',
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
    date_start = models.DateField(verbose_name='Дата начала мероприятия', null=True, blank=True)
    date_end = models.DateField(verbose_name='Дата окончания мероприятия', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=100,
        verbose_name='Статус мероприятия',
        choices=STATUS_CHOICES,
        default=STATUS_WAIT
    )

    def __str__(self):
        return f'Мероприятие "{self.name}" дата: {self.date_start}-{self.date_end}'

    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'pk': self.pk})

    def get_redirect_url_for_event_list(self):
        return self.get_absolute_url()

    def get_avg_grade(self):
        return Grade.objects.filter(event=self).aggregate(models.Avg('grade'))['grade__avg']

    def get_grade(self):
        try:
            return Grade.objects.get(event=self).grade
        except:
            return 0

    class Meta:
        ordering = ['date_start']
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

    event = models.ForeignKey('Event', verbose_name='Мероприятие', null=True, blank=True, on_delete=models.CASCADE)
    server = models.ForeignKey('Server', verbose_name='Сервер', on_delete=models.CASCADE, null=True, blank=True)
    quota = models.PositiveSmallIntegerField(verbose_name='Количество участников', null=True, blank=True)
    link = models.CharField(max_length=255, verbose_name='Ссылка', null=True, blank=True)
    date = models.DateField(verbose_name='Дата проведения')
    time_start = models.TimeField(verbose_name='Время начала')
    time_end = models.TimeField(verbose_name='Время окончания')
    created_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=100,
        verbose_name='Статус видеоконференции',
        choices=STATUS_CHOICES,
        default=STATUS_WAIT
    )
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)

    def __str__(self):
        return f'Конференция на "{self.server}" запланирована на {self.date} с {self.time_start} по {self.time_end}'

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
        'update': 'Бронирование изменено!',
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
    conference = models.ForeignKey('Conference', verbose_name='Конференция', null=True, blank=True,
                                   on_delete=models.CASCADE)
    without_conference = models.BooleanField(verbose_name='Без конференции', default=False)
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
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)

    def __str__(self):
        return f'Помещение "{self.room}" забронировано на {self.date} с {self.time_start} по {self.time_end}'

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


class Server(models.Model):

    SERVER_TYPE_EXTERNAL = 'external'
    SERVER_TYPE_LOCAL = 'local'

    SERVER_TYPE_CHOICES = (
        (SERVER_TYPE_EXTERNAL, 'Внешний сервер'),
        (SERVER_TYPE_LOCAL, 'Внутренний сервер')
    )

    name = models.CharField(max_length=255, verbose_name='Название сервера')
    application = models.ForeignKey('Application', verbose_name='Приложение', null=True, blank=True,
                                    on_delete=models.CASCADE)
    server_address = models.CharField(max_length=50, verbose_name='Адрес сервера', null=True, blank=True)
    quota = models.PositiveSmallIntegerField(verbose_name='Количество лицензий', null=True, blank=True)
    responsible = models.ForeignKey('Staffer', verbose_name='Ответственный сотрудник', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    server_type = models.CharField(
        max_length=100,
        verbose_name='Тип сервера',
        choices=SERVER_TYPE_CHOICES,
        default=SERVER_TYPE_LOCAL
    )

    def __str__(self):
        if self.application:
            return f'{self.server_type} - {self.name } - {self.application}'
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Сервер'
        verbose_name_plural = 'Сервера'


class Application(models.Model):

    name = models.CharField(max_length=255, verbose_name='Название приложения')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Приложение'
        verbose_name_plural = 'Приложения'


class Staffer(models.Model):

    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.PROTECT)
    name = models.CharField(max_length=255, verbose_name='ФИО')
    email = models.EmailField(verbose_name='Электронная почта', null=True, blank=True,)
    subscribe_mail = models.BooleanField(verbose_name='Подписка на почтовую рассылку', default=False)
    telegram = models.CharField(max_length=10, verbose_name='Телеграм чат-id', null=True, blank=True,)
    subscribe_telegram = models.BooleanField(verbose_name='Подписка на рассылку в телеграм', default=False)
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

