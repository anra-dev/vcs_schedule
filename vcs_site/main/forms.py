from django import forms

from .models import Event, Application


class EventAddForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['date'].label = 'Дата проведения'
    #     self.fields['time_start'].label = 'Время начала'
    #     self.fields['time_end'].label = 'Время окончания'

    date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    time_start = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}))
    time_end = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}))

    class Meta:
        model = Event
        fields = (
            '__all__'
        )

    def clean(self):
        """Валидация формы"""
        date = self.cleaned_data['date']
        time_start = self.cleaned_data['time_start']
        time_end = self.cleaned_data['time_end']
        number_of_participants = self.cleaned_data['number_of_participants']
        application = self.cleaned_data['application']

        # Начало должно быть раньше конца
        if time_start > time_end:
            self.add_error('time_start', 'Время начала не может быть позже окончания')
            self.add_error('time_end', 'Время окончания не может быть раньше начала')

        # Время не должно быть занято кем то ранее
        events_on_this_date = Event.objects.filter(date=date)
        for event in events_on_this_date:
            if (event.time_start <= time_start < event.time_end) or (time_start <= event.time_start < time_end):
                self.add_error('time_start', 'Время занято другим мероприятием')
                self.add_error('time_end', 'Время занято другим мероприятием')

        # Количество участников не може превышать количество лицензий
        number_of_participants = self.cleaned_data['number_of_participants']
        application = self.cleaned_data['application']
        if number_of_participants > application.number_of_licenses:
            self.add_error('number_of_participants', f'Количество участников превышает '
                                                     f'количество лицензий для программы "{application.name}"')

        return self.cleaned_data
