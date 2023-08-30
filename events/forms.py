from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ('created_on',)
        widgets = {
            'start_time': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local'}),
        }
