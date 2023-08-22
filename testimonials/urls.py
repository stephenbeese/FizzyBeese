from django.urls import path
from .views import TestimonialView
from . import views

urlpatterns = [
    path('', TestimonialView.as_view(), name='testimonial'),
]
