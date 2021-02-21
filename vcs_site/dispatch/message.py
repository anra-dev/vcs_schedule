from schedule.models import Staffer


def get_message(obj=None):
    print('Function get_message')
    return 'Тест'


def get_recipients(obj=None):
    staffers = Staffer.objects.all()
    recipients = {'mail': [], 'telegram': []}
    for staffer in staffers:
        recipients['mail'].append(staffer.email)
        recipients['telegram'].append(staffer.telegram)
    print(recipients)
    return recipients, staffers
