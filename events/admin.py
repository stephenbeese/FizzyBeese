from django.contrib import admin
from .models import Event


class EventAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'start_time', 'end_time',
              'street_address1', 'street_address2', 'town_or_city',
              'county', 'postcode', 'organiser',)
    readonly_fields = ('created_on',)


admin.site.register(Event)
