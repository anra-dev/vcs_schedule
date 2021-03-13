from schedule.models import Booking, Conference


def get_message(event=None):
    conferences = Conference.objects.filter(event=event).exclude(booking__without_conference=False)
    bookings = Booking.objects.filter(event=event)
    print('Queryset conference:', conferences)
    print('Queryset booking:', bookings)
    message = f'----------------------------------\n'
    message += f'Мероприятие {event.name } - полностью готово к проведению \n'
    message += f'Организатор: {event.organization } \n'
    message += f'Ответственный сотрудник: {event.responsible} \n'
    message += f'Телефон: {event.responsible.phone}, '
    message += f'электронная почта: {event.responsible.email} \n'
    message += f'Дата проведения: {event.date_start}-{event.date_end} \n'
    message += f'----------------------------------\n'
    i = 1
    for conference in conferences:
        message += f'Сессия №{i}\n'
        message += f'время проведения с {conference.time_start} по  {conference.time_end}\n'
        message += f'Сервер:  {conference.server}\n'
        message += f'Ссылка: {conference.link}\n'
        message += f'Ответственный сотрудник: {conference.responsible} \n'
        message += f'Телефон: {conference.responsible.phone}, '
        message += f'электронная почта: {conference.responsible.email} \n'
        message += f'----без бронирования помещения----\n'
        message += f'----------------------------------\n'
        i += 1
    for booking in bookings:
        message += f'Сессия №{i}\n'
        message += f'время проведения с {booking.time_start} по  {booking.time_end}\n'
        message += f'Помещение {booking.room}\n'
        message += f'Ответственный сотрудник: {booking.responsible} \n'
        message += f'Телефон: {booking.responsible.phone}, '
        message += f'электронная почта: {booking.responsible.email} \n'
        if not booking.without_conference:
            message += f'Подключение конференции:  {booking.conference.server}\n'
            message += f'Ссылка: {booking.conference.link}\n'
            message += f'Ответственный сотрудник: {booking.conference.responsible} \n'
            message += f'Телефон: {booking.conference.responsible.phone}, '
            message += f'электронная почта: {booking.conference.responsible.email} \n'
        message += f'----------------------------------\n'
        i += 1
    return message


def get_recipients(event=None):
    print('Function get_recipients begins')
    responsibles = [booking.responsible for booking in Booking.objects.filter(event=event)]
    responsibles.append(event.responsible)

    recipients = {'mail': [], 'telegram': []}
    for responsible in set(responsibles):
        if responsible.subscribe_mail:
            recipients['mail'].append(responsible.email)
        if responsible.subscribe_telegram:
            recipients['telegram'].append(responsible.telegram)
    print('Function get_recipients:', recipients)
    return recipients, responsibles
