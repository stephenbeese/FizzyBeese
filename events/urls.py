from django.urls import path
from .views import CreateEvent, Events

urlpatterns = [
    path('create/', CreateEvent.as_view(), name='create_event'),
    path('', Events.as_view(), name='events_list'),
]
