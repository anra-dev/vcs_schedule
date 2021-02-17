from django import forms
from django.contrib.auth import get_user_model
import datetime

from .models import Event, Conference, Booking, Room
from .services import check_ability_to_create_conf, check_room_is_free

User = get_user_model()

my_default_errors = {
    'required': 'Это поле обязательное',
    'invalid': 'Некореектное значение'
}


class EventAddForm(forms.ModelForm):
    """
    Форма для создания мероприятия
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].label = 'Дата проведения'

    date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < datetime.date.today():
            self.add_error('date', 'Некорректная дата')
        return date

    class Meta:
        model = Event
        fields = (
            'name',
            'description',
            'date',
        )


class ConferenceAddForm(forms.ModelForm):
    """
    Форма для внутренней видеоконференции
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['event'].widget.attrs['readonly'] = True
        self.fields['date'].widget.attrs['readonly'] = True
        self.fields['time_start'].label = 'Время начала'
        self.fields['time_end'].label = 'Время окончания'

    time_start = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}))
    time_end = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}))

    def clean(self):
        """Валидация формы"""
        time_start = self.cleaned_data['time_start']
        time_end = self.cleaned_data['time_end']
        quota = self.cleaned_data['quota']
        application = self.cleaned_data['application']
        date = self.cleaned_data['date']
        type = self.cleaned_data['type']
        conf_id = self.instance.id  # почему не падает при создании конфы если равно None?

        # Начало должно быть раньше конца
        if time_start >= time_end:
            self.add_error('time_start', 'Время начала не может совпадать или быть позже окончания')
            self.add_error('time_end', 'Время окончания не может совпадать или быть раньше начала')
        # Проверка на наличие свободных лицензий
        if type == 'local':
            if not check_ability_to_create_conf(conf_id=conf_id, application=application, date=date, time_start=time_start,
                                                time_end=time_end, quote=quota):
                self.add_error('quota', 'Превышено количество пользователей (учитываются все уже назначенный '
                                        'конференции). Измените количество участников или время проведения')
        return self.cleaned_data

    class Meta:
        model = Conference
        fields = (
            'event',
            'date',
            'application',
            'type',
            'quota',
            'link_to_event',
            'application',
            'time_start',
            'time_end',
        )
        widgets = {
            'event': forms.HiddenInput(),
            'date': forms.HiddenInput(),
        }


class BookingAddForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['event'].widget.attrs['readonly'] = True
        self.fields['date'].widget.attrs['readonly'] = True
        self.fields['time_start'].label = 'Время начала'
        self.fields['time_end'].label = 'Время окончания'

    time_start = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}))
    time_end = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}))

    def clean(self):
        """Валидация формы"""
        time_start = self.cleaned_data['time_start']
        time_end = self.cleaned_data['time_end']
        quota = self.cleaned_data['quota']
        room = self.cleaned_data['room']
        date = self.cleaned_data['date']
        booking_id = self.instance.id

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
            self.add_error('quota', f'Количество участников превышает вместимость "{room.__str__()}"')
        return self.cleaned_data

    class Meta:
        model = Booking
        fields = (
            'event',
            'date',
            'room',
            'quota',
            'time_start',
            'time_end',
        )
        widgets = {
            'event': forms.HiddenInput(),
            'date': forms.HiddenInput(),
        }


class LoginForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Пользователь с логином {username} не найден в системе')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError('Неверный пароль')
        return self.cleaned_data

    class Meta:
        model = User
        fields = (
            'username',
            'password'
        )

