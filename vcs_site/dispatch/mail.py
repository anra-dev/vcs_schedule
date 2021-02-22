
def send_mail_message(message=None, mail=None):
    print('Function send_email_message begins')
    print(f'Function send_email_message: {mail}')
    print(
        f""""
        На адрес электронной почты {mail}
        Отправлено следующее сообщение:
        {message}
        """
    )
