# Шаблона сообщений

def get_message_conferences(event):
    message = f'---------Видео конференция---------\n'
    message += f'Сервер:  {event.conf_server}\n'
    message += f'Ссылка: {event.conf_link}\n'
    message += f'Оператор: {event.conf_operator} \n'
    message += f'Телефон: {event.conf_operator.phone}, '
    message += f'электронная почта: {event.conf_operator.email} \n'
    message += f'----------------------------------\n'
    return message


def get_message_bookings(event):
    message = f'------Забронировано помещение------\n'
    message += f'Помещение {event.booking_room}\n'
    message += f'Ассистент: {event.booking_assistant} \n'
    message += f'Телефон: {event.booking_assistant.phone}, '
    message += f'электронная почта: {event.booking_assistant.email} \n'
    message += f'----------------------------------\n'
    return message


def get_message_event_ready(event):
    message = f'----------------------------------\n'
    message += f'Мероприятие {event.name}\n'
    message += f'полностью готово к проведению\n'
    message += f'Организатор: {event.organization}\n'
    message += f'Ответственный сотрудник: {event.owner}\n'
    message += f'Телефон: {event.owner.phone}, '
    message += f'электронная почта: {event.owner.email}\n'
    message += f'Дата проведения: {event.date}\n'
    message += f'Время проведения: {event.time_start}-{event.time_end} \n'
    message += f'----------------------------------\n'
    if event.with_booking:
        message_booking = get_message_bookings(event)
        message += message_booking
    else:
        message += f'----без бронирования помещения----\n'
    if event.with_conf:
        message_conf = get_message_conferences(event)
        message += message_conf
    else:
        message += f'-------без конференции---------\n'
    return message


