from django.db import models
from profiles.models import UserProfile


class Testimonial(models.Model):
    """ Model to store user testimonials """
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                                     related_name='testimonials')
    name = models.CharField(max_length=50, null=False, blank=False)
    body = models.TextField(null=False, blank=False)
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Testimonial from {self.name}'
