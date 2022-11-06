import datetime

from django import forms

from schedule.enums import ServerTypeEnum, StatusEnum
from schedule.models import Event
from schedule.api import check_free_quota, check_room_is_free


my_default_errors = {
    'required': 'Это поле обязательное',
    'invalid': 'Некорректное значение'
}


class CustomSelectWidget(forms.Select):

    def create_option(self, name, value, label, selected, index,
                      subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index)
        if value:
            option['attrs']['data-server-type'] = value.instance.type
        return option


class EventCreateForm(forms.ModelForm):
    """
    Форма для создания мероприятия
    """
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['date'].widget = forms.TextInput(
            attrs={'type': 'date'})
        self.fields['time_start'].widget = forms.TextInput(
            attrs={'type': 'time'})
        self.fields['time_end'].widget = forms.TextInput(
            attrs={'type': 'time'})
        self.fields['booking_room'].queryset = (
            self.fields['booking_room'].queryset.filter(
                organization__user=self.user,
            )
        )

    def clean_date(self):
        """
        Валидация поля date
        """
        date = self.cleaned_data['date']
        if date < datetime.date.today():
            self.add_error('date', 'Некорректная дата')
        return date

    def clean(self):
        """Валидация формы"""
        cleaned_data = super().clean()
        date = cleaned_data['date']
        time_start = cleaned_data['time_start']
        time_end = cleaned_data['time_end']
        conf_server = cleaned_data['conf_server']
        conf_number_clients = cleaned_data['conf_number_clients']
        booking_room = cleaned_data['booking_room']
        event_id = self.instance.id

        # Начало конференции должно быть раньше ее конца
        if time_start >= time_end:
            self.add_error(
                'time_start',
                'Время начала не может совпадать или быть позже окончания')
            self.add_error(
                'time_end',
                'Время окончания не может совпадать или быть раньше начала')

        if cleaned_data['with_conf']:
            if not conf_server:
                self.add_error('conf_server', my_default_errors['required'])
                return cleaned_data

            if conf_server.type == ServerTypeEnum.SERVER_TYPE_LOCAL:
                cleaned_data['conf_link'] = None
                cleaned_data['conf_note'] = None
                cleaned_data['conf_file'] = ''

                if not conf_number_clients:
                    self.add_error(
                        'conf_number_clients',
                        my_default_errors['required'])
                elif conf_number_clients > conf_server.quota:
                    self.add_error(
                        'conf_number_clients',
                        f'Превышено количество участников для данного '
                        f'сервера! Максимальное число пользователей: '
                        f'{conf_server.quota}')
                else:
                    free_quota = check_free_quota(
                        event_id=event_id,
                        conf_server=conf_server,
                        date=date,
                        time_start=time_start,
                        time_end=time_end,
                    )
                    if free_quota == 0:
                        self.add_error(
                            'conf_number_clients',
                            f'Все лицензии заняты! Выберите другое время')
                    elif conf_number_clients > free_quota:
                        self.add_error(
                            'conf_number_clients',
                            f'Количество участников превышает количество '
                            f'свободных лицензий! На это время свободно '
                            f'всего {free_quota} лицензий')

            if conf_server.type == ServerTypeEnum.SERVER_TYPE_EXTERNAL:
                cleaned_data['conf_number_clients'] = None

                if (not cleaned_data['conf_link']
                        and not cleaned_data['conf_file']
                        and not cleaned_data['conf_note']):

                    msg = 'Хотя бы одно поле должно быть заполнено.'
                    self.add_error('conf_note', msg)
                    self.add_error('conf_link', msg)
                    self.add_error('conf_file', msg)
        else:
            cleaned_data['conf_server'] = None
            cleaned_data['conf_link'] = None
            cleaned_data['conf_note'] = None
            cleaned_data['conf_file'] = ''
            cleaned_data['conf_number_clients'] = None

        if cleaned_data['with_booking']:
            if not booking_room:
                self.add_error('booking_room', my_default_errors['required'])
                return cleaned_data

            room_is_free = check_room_is_free(
                event_id=event_id,
                booking_room=booking_room,
                date=date,
                time_start=time_start,
                time_end=time_end,
            )
            if not room_is_free:
                msg = 'На это время помещение занято другим мероприятием.'
                self.add_error('time_start', msg)
                self.add_error('time_end', msg)
                self.add_error('booking_room', msg)
        else:
            cleaned_data['booking_room'] = None
            cleaned_data['booking_note'] = None

        return cleaned_data

    def save(self, *args, **kwargs):
        if self.cleaned_data['with_booking']:
            self.instance.booking_status = StatusEnum.STATUS_WAIT
        if self.cleaned_data['with_conf']:
            self.instance.conf_status = StatusEnum.STATUS_WAIT
        return super().save(*args, **kwargs)

    class Meta:
        model = Event
        fields = (
            'name',
            'description',
            'date',
            'time_start',
            'time_end',
            'with_conf',
            'conf_server',
            'conf_note',
            'conf_number_clients',
            'conf_file',
            'conf_link',
            'with_booking',
            'booking_room',
            'booking_note',
        )
        widgets = {
            'conf_server': CustomSelectWidget(),
            'description': forms.Textarea(attrs={'rows': 9, 'cols': 40}),
            'conf_note': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
            'booking_note': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
        }


class EventUpdateForm(EventCreateForm):
    """
    Форма для редактирования мероприятия
    """

