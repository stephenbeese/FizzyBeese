from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib import messages

from .forms import EventForm


class CreateEvent(View):
    def get(self, request):
        template = 'events/events_form.html'
        if request.user.is_superuser:
            form = EventForm()
            context = {
                'form': form,
            }
            return render(request, template, context)
        else:
            messages.error(request, 'You need to be an admin to access this page!')
            return redirect(reverse('home'))

    def post(self, request):
        form = EventForm(request.POST)
        if form.is_valid():
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            if start_time > end_time:
                messages.error(request,
                               'start time must be earlier than the end time')
                return redirect('create_event')
            else:
                form.save()
                messages.success(request, 'Event successfully added!')
                return redirect('home')
