from django.conf import settings
from django.core.mail import send_mail


def send_mail_message(message=None, mail=None):
    message += '\n\nС уважением,'
    message += '\nАвтоматическая система оповещения Центра информационных технологий Волгоградской области'
    send_mail(
        subject='Система видеоконференцсвязи',
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[mail],
        fail_silently=False,
    )

