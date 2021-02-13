from django import forms
from django.contrib.auth import get_user_model
import datetime

from .models import Event, VideoConf, ReservedRoom

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


class VideoConfAddForm(forms.ModelForm):
    """
    Форма для внутренней видеоконференции
    """

    def __init__(self, for_event,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event = for_event
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

        # Начало должно быть раньше конца
        if time_start > time_end:
            self.add_error('time_start', 'Время начала не может быть позже окончания')
            self.add_error('time_end', 'Время окончания не может быть раньше начала')

        # Время не должно быть занято кем то ранее
        date = self.event.date
        events_on_this_date = Event.objects.filter(date=date)
        for event in events_on_this_date:
            if event == self.event:
                continue
            video_conf = VideoConf.objects.filter(event=event).first()
            if video_conf:
                if (video_conf.time_start <= time_start < video_conf.time_end) or (time_start <= video_conf.time_start < time_end):
                    self.add_error('time_start', 'Время занято другим мероприятием')
                    self.add_error('time_end', 'Время занято другим мероприятием')

        # Количество участников не може превышать количество лицензий
        if quota > application.quota:
            self.add_error('number_places', f'Количество участников превышает '
                                                     f'количество лицензий для программы "{application.name}"')

        return self.cleaned_data

    class Meta:
        model = VideoConf
        fields = (
            'application',
            'type',
            'quota',
            'link_to_event',
            'application',
            'time_start',
            'time_end',
        )


class ReservedRoomAddForm(forms.ModelForm):

    def __init__(self, for_event,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event = for_event
        self.fields['time_start'].label = 'Время начала'
        self.fields['time_end'].label = 'Время окончания'

    time_start = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}))
    time_end = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}))

    def clean(self):
        """Валидация формы"""
        time_start = self.cleaned_data['time_start']
        time_end = self.cleaned_data['time_end']

        # Начало должно быть раньше конца
        if time_start > time_end:
            self.add_error('time_start', 'Время начала не может быть позже окончания')
            self.add_error('time_end', 'Время окончания не может быть раньше начала')
        return self.cleaned_data

        # # Время не должно быть занято кем то ранее
        # date = self.event.date
        # events_on_this_date = Event.objects.filter(date=date)
        # for event in events_on_this_date:
        #     video_conf = VideoConf.objects.filter(event=event).first()
        #     if video_conf:
        #         if (video_conf.time_start <= time_start < video_conf.time_end) or (
        #                 time_start <= video_conf.time_start < time_end):
        #             self.add_error('time_start', 'Время занято другим мероприятием')
        #             self.add_error('time_end', 'Время занято другим мероприятием')
        #
        # # Количество участников не може превышать количество лицензий
        # if number_places > application.number_of_licenses:
        #     self.add_error('number_places', f'Количество участников превышает '
        #                                     f'количество лицензий для программы "{application.name}"')

    class Meta:
        model = ReservedRoom
        fields = (
            'room',
            'quota',
            'time_start',
            'time_end',
        )


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

