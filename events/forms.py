from django.shortcuts import redirect
from django import forms
from .models import Event
from django.contrib import messages


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ('created_on',)
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    # def clean(self):
    #     cleaned_data = super().clean()
    #     start_time = cleaned_data.get('start_time')
    #     end_time = cleaned_data.get('end_time')

    #     if start_time >= end_time:
    #         messages.error(request, 'The start time is later than the end time \
    #                        Please change this and resubmit the form.')
    #         return redirect('create_event')
