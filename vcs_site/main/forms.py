from django import forms

from .models import Event


class EventDetailForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = (
            '__all__'
        )