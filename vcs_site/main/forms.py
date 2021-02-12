from django import forms
from django.contrib.auth import get_user_model

from .models import Event, VideoConf, ReservedRoom

User = get_user_model()


class EventAddForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].label = 'Дата проведения'

    date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Event
        fields = (
            'name',
            'description',
            'date',
            'type'
        )


class VideoConfAddForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['time_start'].label = 'Время начала'
        self.fields['time_end'].label = 'Время окончания'

    time_start = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}))
    time_end = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}))

    class Meta:
        model = VideoConf
        fields = (
            'number_places',
            'application',
            'link_to_event',
            'time_start',
            'time_end',
        )

    # def clean(self):
    #     """Валидация формы"""
    #     date = self.cleaned_data['date']
    #     time_start = self.cleaned_data['time_start']
    #     time_end = self.cleaned_data['time_end']
    #     number_of_participants = self.cleaned_data['number_of_participants']
    #     application = self.cleaned_data['application']
    #
    #     # Начало должно быть раньше конца
    #     if time_start > time_end:
    #         self.add_error('time_start', 'Время начала не может быть позже окончания')
    #         self.add_error('time_end', 'Время окончания не может быть раньше начала')
    #
    #     # Время не должно быть занято кем то ранее
    #     events_on_this_date = Event.objects.filter(date=date)
    #     for event in events_on_this_date:
    #         if (event.time_start <= time_start < event.time_end) or (time_start <= event.time_start < time_end):
    #             self.add_error('time_start', 'Время занято другим мероприятием')
    #             self.add_error('time_end', 'Время занято другим мероприятием')
    #
    #     # Количество участников не може превышать количество лицензий
    #     number_of_participants = self.cleaned_data['number_of_participants']
    #     application = self.cleaned_data['application']
    #     if number_of_participants > application.number_of_licenses:
    #         self.add_error('number_of_participants', f'Количество участников превышает '
    #                                                  f'количество лицензий для программы "{application.name}"')
    #
    #     return self.cleaned_data


class ReservedRoomAddForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['time_start'].label = 'Время начала'
        self.fields['time_end'].label = 'Время окончания'

    time_start = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}))
    time_end = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}))

    class Meta:
        model = ReservedRoom
        fields = (
            'room',
            'number_places',
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

