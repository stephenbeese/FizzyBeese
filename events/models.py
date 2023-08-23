from django.db import models


class Event(models.Model):
    """
    Model to store upcoming events
    """
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    county = models.CharField(max_length=80, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=False, blank=False)
    organiser = models.CharField(max_length=256, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        """ Orders events by date """
        ordering = ['-start_time']

    def __str__(self):
        return f'{self.title}'
