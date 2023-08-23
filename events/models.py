from django.db import models


class Event(models.Model):
    """
    Model to store upcoming events
    """
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=256, blank=False, null=False)
    organiser = models.CharField(max_length=256, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title