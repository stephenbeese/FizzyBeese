from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    """ 
    Form for user to be able to contact the admin
    """
    class Meta:
        model = Contact
        fields = ('name', 'email', 'subject', 'body',)
        labels = {
            'body': 'Your message...'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'name': 'Full Name',
            'email': 'Email Address',
            'subject': 'Describe your query',
            'body': 'Your enquiry...',
        }

        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
