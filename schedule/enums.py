from django.db import models


EVENT_MESSAGES_DICT = {
    'create': 'Мероприятие создано!',
    'update': 'Мероприятие изменено!',
    'delete': 'Мероприятие удалено!',
    'conf_approve': 'Видеоконференция обработана!',
    'booking_approve': 'Бронирование обработано!',
}


class StatusEnum(models.IntegerChoices):
    """
    Статусы в мероприятии
    """
    STATUS_DRAFT = 1, 'Создание'
    STATUS_WAIT = 2, 'Ожидание'
    STATUS_READY = 3, 'Готово'
    STATUS_REJECTION = 4, 'Отказ'
    STATUS_COMPLETED = 5, 'Окончено'

    @classmethod
    def get_css_class(cls, status):
        css_classes = {
            cls.STATUS_DRAFT: 'info',
            cls.STATUS_WAIT: 'warning',
            cls.STATUS_READY: 'success',
            cls.STATUS_REJECTION: 'danger',
            cls.STATUS_COMPLETED: 'secondary',
        }
        return css_classes.get(status)


class ServerTypeEnum(models.IntegerChoices):
    """
    Тип сервера
    """
    SERVER_TYPE_EXTERNAL = 1, 'Внешний сервер'
    SERVER_TYPE_LOCAL = 2, 'Внутренний сервер'


class GradeEnum(models.IntegerChoices):
    """
    Оценка мероприятия
    """
    GRADE_1 = 1, 'Очень плохо'
    GRADE_2 = 2, 'Плохо'
    GRADE_3 = 3, 'Удовлетворительно'
    GRADE_4 = 4, 'Хорошо'
    GRADE_5 = 5, 'Отлично'
