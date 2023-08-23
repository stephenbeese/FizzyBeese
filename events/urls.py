from django.urls import path
from .views import CreateEvent

urlpatterns = [
    path('create/', CreateEvent.as_view(), name='create_event'),
]
