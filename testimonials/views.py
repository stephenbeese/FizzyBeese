from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.contrib import messages
# from django.contrib.auth.decorators import login_required

from profiles.models import UserProfile
from .forms import TestimonialForm


class TestimonialView(View):
    def get(self, request):
        template = 'testimonials/testimonial_form.html'
        if request.user.is_authenticated:
            form = TestimonialForm()
            context = {
                'form': form
            }

            return render(request, template, context)
        else:
            messages.error(request, 'You need to be logged in to submit a \
                testimonial. Please log in and try again!')
            return redirect(reverse('home'))

    def post(self, request):
        profile = get_object_or_404(UserProfile, user=request.user)
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.user_profile = profile
            testimonial.save()
        
        return redirect(reverse('profile'))

