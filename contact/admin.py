from django.contrib import admin
from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'body', 'created_on')
    fields = ('name', 'subject', 'body', 'created_on')
    readonly_fields = ('user_profile', 'name', 'subject',
                       'body', 'created_on',)
    order_by = '-created_on'


admin.site.register(Contact)
