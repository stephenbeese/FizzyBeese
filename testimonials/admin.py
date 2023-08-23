from django.contrib import admin
from .models import Testimonial


class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'approved', 'created_on')
    fields = ('name', 'body', 'approved', 'created_on')
    readonly_fields = ('created_on',)
    order_by = '-created_on'


admin.site.register(Testimonial)
