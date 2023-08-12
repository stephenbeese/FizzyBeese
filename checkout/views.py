from django.shortcuts import render, redirect, reverse
from django.contrib import messages
# from django.views import View
from django.conf import settings

from .forms import OrderForm
from bag.contexts import bag_contents

import stripe


# class CheckoutView(View):
#     """
#     A view to render the checkout page
#     """

#     def get(self, request, *args, **kwargs):
#         stripe_public_key = settings.STRIPE_PUBLIC_KEY
#         stripe_secret_key = settings.STRIPE_SECRET_KEY
#         bag = request.session.get('bag', {})
#         if not bag:
#             messages.error(request, "Theres nothing in your bag at the moment!")
#             return redirect(reverse('products'))
#         current_bag = bag_contents(request)
#         total = current_bag['grand_total']
#         stripe_total = round(total * 100)
#         stripe.api_key = stripe_secret_key
#         intent = stripe.PaymentIntent.create(
#             amount=stripe_total,
#             currency=settings.STRIPE_CURRENCY,
#         )
#         print(intent)

#         order_form = OrderForm()
#         if not stripe_public_key:
#             messages.warning(request, 'Stripe public key is missing. \
#                 Did you forget to set it in your environment?')

#         template = 'checkout/checkout.html'
#         context = {
#             'order_form': order_form,
#             'stripe_public_key': stripe_public_key,
#             'client_secret': intent.client_secret,
#         }

#         return render(request, template, context)


def checkout(request):
    """
    A view to render the checkout page
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "Theres nothing in your bag at the moment!")
        return redirect(reverse('products'))
    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )
    print(intent)

    order_form = OrderForm()
    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)
