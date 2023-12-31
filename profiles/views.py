from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .models import UserProfile
from .forms import UserProfileForm

from checkout.models import Order


@login_required
def all_orders(request):
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that!')
        return redirect(reverse('home'))

    orders = Order.objects.all().order_by('-date')
    template = 'profiles/all_orders.html'
    context = {
        'orders': orders,
    }
    return render(request, template, context)


@login_required
def profile(request):
    """ Display the user's profile """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(
                request, 'Update failed. Please ensure the form is vaild.')
    else:
        form = UserProfileForm(instance=profile)

    orders = profile.orders.all().order_by('-date')
    testimonials = profile.testimonials.all().order_by('-created_on')
    template = 'profiles/profile.html/'
    context = {
        'form': form,
        'orders': orders,
        'testimonials': testimonials,
        'on_profile_page': True,
    }

    return render(request, template, context)


def order_history(request, order_number):
    """
    Displays a users past order using
    the checkout success template
    """
    if request.user.is_authenticated:
        order = get_object_or_404(Order, order_number=order_number)
        messages.info(request, (
            f'This is a past confirmation for order number {order_number}.'
            'A confirmation email was sent on the order date.'
        ))

        template = 'checkout/checkout_success.html'
        context = {
            'order': order,
            'from_profile': True,
        }

        return render(request, template, context)
    else:
        messages.error(request, 'You need to be logged in to view this page, \
                       please login and try again!')
        return redirect('home')
