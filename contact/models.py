from django.db import models
from profiles.models import UserProfile


class Contact(models.Model):
    """
    Model for user to contact the admin
    """
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                                     related_name='contact')
    name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    subject = models.CharField(max_length=100, null=False, blank=False)
    body = models.TextField(null=False, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.name}: {self.subject}'
