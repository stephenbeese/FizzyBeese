from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.contrib import messages

from profiles.models import UserProfile
from .forms import ContactForm
from .models import Contact


class ContactView(View):
    def get(self, request):
        template = 'contact/contact.html'
        # if request.user.is_authenticated:
        form = ContactForm()
        context = {
            'form': form
        }

        return render(request, template, context)
        # else:
        #     messages.error(request, 'You need to be logged in to submit a \
        #         testimonial. Please log in and try again!')
        #     return redirect(reverse('home'))

    def post(self, request):
        if request.user.is_authenticated:
            profile = get_object_or_404(UserProfile, user=request.user)
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            if request.user.is_authenticated:
                contact.user_profile = profile
            contact.save()
        
        return redirect(reverse('home'))
