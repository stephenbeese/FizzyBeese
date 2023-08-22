from django import forms
from .models import Testimonial


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ('name', 'body',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'name': 'Full Name',
            'body': 'Tell us what you think!',
        }

        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
