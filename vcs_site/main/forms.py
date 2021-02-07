from django import forms

from .models import Event


class EventAddForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = (
            '__all__'
        )