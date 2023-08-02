from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):
    bag_items = []
    total = 0
    product_count = 0
    total_weight = 0
    bag = request.session.get('bag', {})

    for item_id, quantity in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        # total += quantity * product.price
        product_count += quantity
        total_weight += quantity * product.weight
        if product.sale_price:
            total += quantity * product.sale_price
        else:
            total += quantity * product.price

        bag_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
        })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        if product_count == 0:
            delivery = 0
        else:
            # Calculate shipping by weight in grams
            if total_weight <= 100:
                delivery = Decimal(1.60)
            elif total_weight <= 2000:
                delivery = Decimal(3.69)
            else:
                delivery = Decimal(5.29)

        # delivery = round(delivery, 2)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'total_weight': total_weight,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
