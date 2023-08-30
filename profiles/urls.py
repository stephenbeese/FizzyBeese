from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path(
        '',
        views.profile,
        name='profile'),
    path(
        'all_orders/',
        views.all_orders,
        name='all_orders'),
    path(
        'order_history/<order_number>',
        views.order_history,
        name='order_history'),
]
