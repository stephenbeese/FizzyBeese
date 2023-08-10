from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


# @admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)
    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'total_weight',
                       'order_total', 'grand_total',)

    list_display = ('order_number', 'date', 'full_name',
                    'total_weight', 'delivery_cost',
                    'order_total', 'grand_total')

    order_by = ('-date')


admin.site.register(Order, OrderAdmin)
