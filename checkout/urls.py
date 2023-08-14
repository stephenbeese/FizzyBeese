from django.urls import path
from .views import CheckoutView
from . import views

urlpatterns = [
    path('', CheckoutView.as_view(), name='checkout'),
    path('success/<order_number>', views.checkout_success, name='checkout_success'),
]
