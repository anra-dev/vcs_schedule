from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Event(models.Model):

    STATUS_CREATED = 'created'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = (
        (STATUS_CREATED, 'Заявка'),
        (STATUS_READY, 'Одобрено'),
        (STATUS_COMPLETED, 'Окончено')
    )

    TYPE_LOCAL = 'local'
    TYPE_EXTERNAL = 'external'
    TYPE_WITHOUT_VCS = 'without_vcs'

    TYPE_CHOICES = (
        (TYPE_LOCAL, 'Внутренняя видеоконференция'),
        (TYPE_EXTERNAL, 'Внешняя видеоконференция'),
        (TYPE_WITHOUT_VCS, 'Без видеоконференции')
    )

    name = models.CharField(max_length=255, verbose_name='Название мероприятия')
    description = models.TextField(verbose_name='Описание')
    organization = models.ForeignKey('Organization', verbose_name='Организация', on_delete=models.CASCADE)
    responsible = models.ForeignKey('Staffer', verbose_name='Ответственный сотрудник', on_delete=models.CASCADE)
    date = models.DateField(verbose_name='Дата проведения')
    type = models.CharField(
        max_length=100,
        verbose_name='Тип мероприятия',
        choices=TYPE_CHOICES,
        default=TYPE_LOCAL,
        help_text="Please type your age."
    )
    status = models.CharField(
        max_length=100,
        verbose_name='Статус мероприятия',
        choices=STATUS_CHOICES,
        default=STATUS_CREATED
    )
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Мероприятие "{self.name}" запланировано на {self.date}'


class VideoConf(models.Model):

    event = models.ForeignKey('Event', verbose_name='Мероприятие', null=True, blank=True, on_delete=models.CASCADE)
    number_places = models.PositiveSmallIntegerField(verbose_name='Количество участников')
    application = models.ForeignKey('Application', verbose_name='Приложение', null=True, blank=True, on_delete=models.CASCADE)
    link_to_event = models.CharField(max_length=255, verbose_name='Ссылка', null=True, blank=True)
    time_start = models.TimeField(verbose_name='Время начала мероприятия')
    time_end = models.TimeField(verbose_name='Время окончания мероприятия')


class ReservedRoom(models.Model):

    event = models.ForeignKey('Event', verbose_name='Мероприятие', null=True, blank=True, on_delete=models.CASCADE)
    room = models.ForeignKey('Room', verbose_name='Место проведения', null=True, blank=True, on_delete=models.CASCADE)
    number_places = models.PositiveSmallIntegerField(verbose_name='Количество участников')
    time_start = models.TimeField(verbose_name='Время начала мероприятия')
    time_end = models.TimeField(verbose_name='Время окончания мероприятия')


class Organization(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название организации')
    responsible = models.ForeignKey('Staffer', verbose_name='Ответственный сотрудник', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Room(models.Model):
    address = models.CharField(max_length=255, verbose_name='Адрес')
    room = models.CharField(max_length=255, verbose_name='Комната')
    capacity = models.PositiveIntegerField(verbose_name='Вместимость')
    responsible = models.ForeignKey('Staffer', verbose_name='Ответственный сотрудник', on_delete=models.CASCADE)
    applications = models.ManyToManyField('Application', verbose_name='Приложения', related_name='related_room')

    def __str__(self):
        return f'{self.address} {self.room}'


class Application(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название приложения')
    server_name = models.CharField(max_length=50, verbose_name='Имя сервера')
    number_of_licenses = models.PositiveSmallIntegerField(verbose_name='Количество лицензий')
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
