from django import forms
import datetime

from .models import Event, Conference, Booking, Server
from .services import check_free_quota, check_room_is_free


my_default_errors = {
    'required': 'Это поле обязательное',
    'invalid': 'Некореектное значение'
}


class CustomSelectWidget(forms.Select):

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index)
        if value:
            server = self.choices.queryset.get(pk=str(value))  # get server instance
            option['attrs']['data-server-type'] = server.server_type  # set option attribute
        return option


class EventCreateForm(forms.ModelForm):
    """
    Форма для создания мероприятия
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Event
        fields = (
            'name',
            'description',
        )


class EventUpdateForm(EventCreateForm):
    """
    Форма для редактирования мероприятия
    """


class ConferenceCreateForm(forms.ModelForm):
    """
    Форма создания конференции
    """
    date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    time_start = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}))
    time_end = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}))

    def __init__(self, *args, **kwargs):
        event_id = kwargs.pop('event_id')
        super().__init__(*args, **kwargs)
        self.fields['date'].label = 'Дата проведения'
        self.fields['time_start'].label = 'Время начала'
        self.fields['time_end'].label = 'Время окончания'
        self.event = Event.objects.get(pk=event_id)

    def clean_event(self):
        # защита от подмены на стороне клиента. Пока ищу более правильный способ.
        return self.event

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < datetime.date.today():
            self.add_error('date', 'Некорректная дата')
        return date

    def clean(self):
        """Валидация формы"""
        cleaned_data = super().clean()
        time_start = cleaned_data['time_start']
        time_end = cleaned_data['time_end']
        quota = cleaned_data['quota']
        server = cleaned_data['server']
        link = cleaned_data['link']
        file = cleaned_data['file']
        date = cleaned_data['date']
        description = cleaned_data['description']
        conf_id = self.instance.id

        # Начало конференции должно быть раньше ее конца
        if time_start >= time_end:
            self.add_error('time_start', 'Время начала не может совпадать или быть позже окончания')
            self.add_error('time_end', 'Время окончания не может совпадать или быть раньше начала')

        # Проверка для локальных серверов
        if server.server_type == server.SERVER_TYPE_LOCAL:
            # Очищаем поля не предусмотренные для заполнения пользователем для конференций на локальных серверах
            cleaned_data['link'] = None
            cleaned_data['description'] = None
            cleaned_data['file'] = ''  # Почему то None не удаляет значение из базы

            # Проверка полей
            if not quota:
                # Квота обязательное поле
                self.add_error('quota', my_default_errors['required'])
            elif quota > server.quota:
                # Квота не должна превышать квоту сервера
                self.add_error('quota', f'Превышено количество участников для данного приложения! '
                                        f'Максимальное число пользователей: {server.quota}')
            else:
                # Проверка свободных квот на сервере на предполагаемое время
                free_quota = check_free_quota(conf_id=conf_id, server=server, date=date,
                                              time_start=time_start, time_end=time_end)
                if free_quota == 0:
                    # Все квоты заняты
                    self.add_error('quota', f'Все лицензии заняты! Выберите другое время')
                elif quota > free_quota:
                    # Запрашиваемые квоты больше чем свободные квоты
                    self.add_error('quota', f'Количество участников превышает количество свободных лицензий!'
                                            f' На это время свободно всего {free_quota} лицензий')

        # Проверка для внешних серверов
        if server.server_type == server.SERVER_TYPE_EXTERNAL:
            # Очищаем поля не предусмотренные для заполнения пользователем для конференций на внешних серверах
            cleaned_data['quota'] = None

            # Проверка полей
            if not description:
                # Квота обязательное поле
                self.add_error('description', my_default_errors['required'])

            # Поле Ссылка или Файл не должны быть пустыми
            if not link and not file:
                raise forms.ValidationError(f"Необходимо заполнить поле {self.fields['link'].label} или "
                                            f"{self.fields['file'].label}")
        return cleaned_data

    class Meta:
        model = Conference
        fields = (
            'event',
            'server',
            'quota',
            'link',
            'description',
            'file',
            'date',
            'time_start',
            'time_end',
        )
        widgets = {
            'event': forms.HiddenInput(),
            'server': CustomSelectWidget(),
        }

        class Media:
            js = ('js/base.js',)  # Проверять на проде


class ConferenceUpdateForm(ConferenceCreateForm):
    """
    Форма для редактирования мероприятия
    """


class BookingCreateForm(forms.ModelForm):
    """
    Форма создания бронирования помещения
    """
    date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    time_start = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}), required=False)
    time_end = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}), required=False)

    def __init__(self, *args, **kwargs):
        event_id = kwargs.pop('event_id')
        super().__init__(*args, **kwargs)
        self.fields['date'].label = 'Дата проведения'
        self.fields['time_start'].label = 'Время начала'
        self.fields['time_end'].label = 'Время окончания'
        self.event = Event.objects.get(pk=event_id)
        conference = Conference.objects.filter(event=self.event)
        self.fields['conference'].queryset = conference

        if not conference:
            self.fields['without_conference'].initial = True
            # self.fields['without_conference'].widget.attrs['disabled'] = True  # fix me!

    def clean_date(self):
        date = self.cleaned_data['date']
        if date:
            if date < datetime.date.today():
                self.add_error('date', 'Некорректная дата')
        return date

    def clean_event(self):
        # защита от подмены на стороне клиента. Пока ищу более правильный способ.
        return self.event

    def clean(self):
        """Валидация формы"""
        cleaned_data = super().clean()
        quota = cleaned_data['quota']
        room = cleaned_data['room']
        booking_id = self.instance.id
        without_conference = cleaned_data['without_conference']
        conference = cleaned_data['conference']

        # Проверяем есть ли связанная конференция
        if without_conference:
            date = cleaned_data['date']
            time_start = cleaned_data['time_start']
            time_end = cleaned_data['time_end']
            cleaned_data['conference'] = None
        else:
            if conference:
                date = cleaned_data['date'] = conference.date
                time_start = cleaned_data['time_start'] = conference.time_start
                time_end = cleaned_data['time_end'] = conference.time_end
            else:
                raise forms.ValidationError('Необходимо указать конференцию')

        # Начало должно быть раньше конца
        if time_start >= time_end:
            self.add_error('time_start', 'Время начала не может совпадать или быть позже окончания')
            self.add_error('time_end', 'Время окончания не может совпадать или быть раньше начала')

        # Время не должно быть занято кем то ранее
        if check_room_is_free(booking_id, room, date, time_start, time_end):
            self.add_error('time_start', 'Время занято другим мероприятием')
            self.add_error('time_end', 'Время занято другим мероприятием')

        # Количество участников не должно превышать вместимость комнаты
        if quota > room.quota:
            self.add_error('quota', f'Максимальное количество мест для этого помещения: {room.quota}')
        return cleaned_data

    class Meta:
        model = Booking
        fields = (
            'event',
            'without_conference',
            'conference',
            'room',
            'quota',
            'date',
            'time_start',
            'time_end',
        )
        widgets = {
            'event': forms.HiddenInput(),
        }


class BookingUpdateForm(BookingCreateForm):
    """
    Форма для редактирования бронирования помещения
    """
    pass
