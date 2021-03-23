from schedule.models import Booking, Conference


def get_message(event=None):
    conferences = Conference.objects.filter(event=event).exclude(booking__without_conference=False)
    bookings = Booking.objects.filter(event=event)
    message = f'----------------------------------\n'
    message += f'Мероприятие {event.name } - полностью готово к проведению \n'
    message += f'Организатор: {event.organization } \n'
    message += f'Ответственный сотрудник: {event.owner} \n'
    message += f'Телефон: {event.owner.phone}, '
    message += f'электронная почта: {event.owner.email} \n'
    message += f'Дата проведения: {event.date_start}-{event.date_end} \n'
    message += f'----------------------------------\n'
    i = 1
    for conference in conferences:
        message += f'Сессия №{i}\n'
        message += f'время проведения с {conference.time_start} по  {conference.time_end}\n'
        message += f'Сервер:  {conference.server}\n'
        message += f'Ссылка: {conference.link}\n'
        message += f'Оператор: {conference.operator} \n'
        message += f'Телефон: {conference.operator.phone}, '
        message += f'электронная почта: {conference.operator.email} \n'
        message += f'----без бронирования помещения----\n'
        message += f'----------------------------------\n'
        i += 1
    for booking in bookings:
        message += f'Сессия №{i}\n'
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
        message += f'----------------------------------\n'
        i += 1
    return message


def get_recipients(event=None):
    users = [booking.assistant for booking in Booking.objects.filter(event=event)]
    users.append(event.owner)

    recipients = {'mail': [], 'telegram': []}
    for user in set(users):
        if user.subscribe_mail:
            recipients['mail'].append(user.email)
        if user.subscribe_telegram:
            recipients['telegram'].append(user.telegram)
    return recipients, users
