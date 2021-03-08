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
    server = forms.ModelChoiceField(queryset=Server.objects.all(), widget=CustomSelectWidget)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['event'].widget.attrs['readonly'] = True
        self.fields['server'].label = 'Сервер'
        self.fields['date'].label = 'Дата проведения'
        self.fields['time_start'].label = 'Время начала'
        self.fields['time_end'].label = 'Время окончания'

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < datetime.date.today():
            self.add_error('date', 'Некорректная дата')
        return date

    def clean(self):
        """Валидация формы"""
        time_start = self.cleaned_data['time_start']
        time_end = self.cleaned_data['time_end']
        quota = self.cleaned_data['quota']
        server = self.cleaned_data['server']
        link = self.cleaned_data['link']
        date = self.cleaned_data['date']
        conf_id = self.instance.id  # почему не падает при создании конфы если равно None?
        # Начало должно быть раньше конца
        if time_start >= time_end:
            self.add_error('time_start', 'Время начала не может совпадать или быть позже окончания')
            self.add_error('time_end', 'Время окончания не может совпадать или быть раньше начала')
        # Проверка на наличие свободных лицензий и обязателых полей
        if server.server_type == 'local':
            if not quota:
                self.add_error('quota', my_default_errors['required'])
            elif quota > server.quota:
                self.add_error('quota', f'Превышено количество участников для данного приложения! '
                                        f'Максимальное число пользователей: {server.quota}')
            else:
                free_quota = check_free_quota(conf_id=conf_id, server=server, date=date,
                                              time_start=time_start, time_end=time_end)
                if free_quota == 0:
                    self.add_error('quota', f'Все лицензии заняты! Выберите другое время')
                elif quota > free_quota:
                    self.add_error('quota', f'Количество участников превышает количество свободных лицензий!'
                                            f' На это время свободно всего {free_quota} лицензий')
        if server.server_type == 'external':
            if not link:
                self.add_error('link', my_default_errors['required'])
        return self.cleaned_data

    class Meta:
        model = Conference
        fields = (
            'event',
            'server',
            'quota',
            'link',
            'date',
            'time_start',
            'time_end',
        )
        widgets = {
            'event': forms.HiddenInput(),
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
        super().__init__(*args, **kwargs)
        self.fields['event'].widget.attrs['readonly'] = True
        self.fields['date'].label = 'Дата проведения'
        self.fields['time_start'].label = 'Время начала'
        self.fields['time_end'].label = 'Время окончания'
        self.fields['conference'].label = 'Конференция'
        self.fields['conference'].widget.attrs['required'] = False
        self.event = self.initial['event']
        conference = Conference.objects.filter(event=self.event)
        self.fields['conference'] = forms.ModelChoiceField(queryset=conference, required=False)
        self.fields['conference'].label = 'Конференция'
        if not conference:
            self.fields['without_conference'].initial = True

    # def clean_date(self):
    #     date = self.cleaned_data['date']
    #     if date < datetime.date.today():
    #         self.add_error('date', 'Некорректная дата')
    #     return date

    def clean(self):
        """Валидация формы"""
        quota = self.cleaned_data['quota']
        room = self.cleaned_data['room']
        booking_id = self.instance.id
        without_conference = self.cleaned_data['without_conference']
        conference = self.cleaned_data['conference']

        # Проверяем есть ли связанная конференция
        if without_conference:
            date = self.cleaned_data['date']
            time_start = self.cleaned_data['time_start']
            time_end = self.cleaned_data['time_end']
            self.cleaned_data['conference'] = None
        else:
            date = self.cleaned_data['date'] = conference.date
            time_start = self.cleaned_data['time_start'] = conference.time_start
            time_end = self.cleaned_data['time_end'] = conference.time_end

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
        return self.cleaned_data

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
