from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.views import View

from .forms import OrderForm


class CheckoutView(View):
    """
    A view to render the checkout page
    """
    def get(self, request, *args, **kwargs):
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "Theres nothing in your bag at the moment!")
            return redirect(reverse('products'))

        order_form = OrderForm()
        template = 'checkout/checkout.html'
        context = {
            'order_form': order_form
        }

        return render(request, template, context)
