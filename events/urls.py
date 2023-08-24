from django.urls import path
from .views import CreateEvent, Events
from . import views

urlpatterns = [
    path('create/', CreateEvent.as_view(), name='create_event'),
    path('', Events.as_view(), name='events_list'),
    path('delete/<int:event_id>', views.delete_event, name='delete_event'),
    path('edit/<int:event_id>', views.edit_event, name='edit_event'),
]
