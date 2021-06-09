# Шаблона сообщений

def get_message_conferences(conferences=None, number=1):
    message = ''
    for conference in conferences:
        message += f'Сессия №{number}\n'
        message += f'время проведения с {conference.time_start} по  {conference.time_end}\n'
        message += f'Сервер:  {conference.server}\n'
        message += f'Ссылка: {conference.link}\n'
        message += f'Оператор: {conference.operator} \n'
        message += f'Телефон: {conference.operator.phone}, '
        message += f'электронная почта: {conference.operator.email} \n'
        message += f'----без бронирования помещения----\n'
        message += f'----------------------------------\n'
        number += 1
    return message, number


def get_message_bookings(bookings=None, number=1):
    message = ''
    for booking in bookings:
        message += f'Сессия №{number}\n'
        message += f'время проведения с {booking.time_start} по  {booking.time_end}\n'
        message += f'Помещение {booking.room}\n'
        message += f'Ассистент: {booking.assistant} \n'
        message += f'Телефон: {booking.assistant.phone}, '
        message += f'электронная почта: {booking.assistant.email} \n'
        if not booking.without_conference:
            message += f'Подключение конференции:  {booking.conference.server}\n'
            message += f'Ссылка: {booking.conference.link}\n'
            message += f'Оператор: {booking.conference.operator} \n'
            message += f'Телефон: {booking.conference.operator.phone}, '
            message += f'электронная почта: {booking.conference.operator.email} \n'
        else:
            message += f'-------без конференции---------\n'
        message += f'----------------------------------\n'
        number += 1
    return message, number


def get_message_event_ready(event, conferences, bookings):
    message = f'----------------------------------\n'
    message += f'Мероприятие {event.name} - полностью готово к проведению \n'
    message += f'Организатор: {event.organization} \n'
    message += f'Ответственный сотрудник: {event.owner} \n'
    message += f'Телефон: {event.owner.phone}, '
    message += f'электронная почта: {event.owner.email} \n'
    message += f'Дата проведения: {event.date_start}-{event.date_end} \n'
    message += f'----------------------------------\n'
    number = 1
    if conferences:
        message_conf, number = get_message_conferences(conferences, number)
        message += message_conf
    if bookings:
        message_book, number = get_message_bookings(bookings, number)
        message += message_book
    return message


