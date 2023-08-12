from django.urls import path
# from .views import CheckoutView
from . import views

urlpatterns = [
    # path('', CheckoutView.as_view(), name='checkout')
    path('', views.checkout, name='checkout'),
]
