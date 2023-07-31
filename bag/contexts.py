from django.conf import settings


def bag_contents(request):
    bag_items = []
    total = 0
    product_count = 0
    total_weight = 0

    if total < settings.FREE_DELIVERY_THRESHOLD:
        if product_count == 0:
            delivery = 0
        else:
            # Calculate shipping by weight in grams
            if total_weight <= 100:
                delivery = 1.60
            elif total_weight <= 2000:
                delivery = 3.69
            else:
                delivery = 5.29
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
