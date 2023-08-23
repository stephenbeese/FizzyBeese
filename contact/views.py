from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib import messages

from profiles.models import UserProfile
from .forms import ContactForm


class ContactView(View):
    def get(self, request):
        template = 'contact/contact.html'
        form = ContactForm()
        context = {
            'form': form
        }

        return render(request, template, context)

    def post(self, request):
        if request.user.is_authenticated:
            profile = get_object_or_404(UserProfile, user=request.user)
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            if request.user.is_authenticated:
                contact.user_profile = profile
            contact.save()

            messages.success(request, 'Your enquiry has been submitted.')
            return render(request, 'contact/contact_success.html',
                          {'contact': contact})
        else:
            template = 'contact/contact.html'
            context = {
                'form': form
            }
            return render(request, template, context)
