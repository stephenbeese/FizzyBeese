from django.utils import timezone
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Event
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
            messages.error(
                request, 'You need to be an admin to access this page!')
            return redirect(reverse('home'))

    def post(self, request):
        form = EventForm(request.POST)
        if form.is_valid():
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            current_time = timezone.now()
            if start_time > end_time:
                messages.error(request,
                               'Start time must be earlier than the end time')
                return redirect('create_event')
            elif start_time <= current_time:
                messages.error(request,
                               'start time must be in the future')
                return redirect('create_event')
            else:
                form.save()
                messages.success(request, 'Event successfully added!')
                return redirect('events_list')


class Events(View):
    def get(self, request):
        current_time = timezone.now()
        future_events = Event.objects.filter(
            start_time__gt=current_time).order_by('start_time')
        template = 'events/events_list.html'
        context = {
            'events': future_events,
        }
        return render(request, template, context)


@login_required
def delete_event(request, event_id):
    """ Delete a product """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that!')
        return redirect(reverse('home'))

    event = get_object_or_404(Event, pk=event_id)
    event.delete()
    messages.success(request, 'Event deleted!')
    return redirect(reverse('events_list'))


@login_required
def edit_event(request, event_id):
    """ Edit a product """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that!')
        return redirect(reverse('home'))

    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated event!')
            return redirect(reverse('events_list'))

        else:
            messages.error(
                request, 'Failed to update please ensure the form is valid.')
    else:
        form = EventForm(instance=event)
        messages.info(request, f'You are currently editing {event.title}')

    template = 'events/edit_event.html'
    context = {
        'form': form,
        'event': event,
    }
    return render(request, template, context)
